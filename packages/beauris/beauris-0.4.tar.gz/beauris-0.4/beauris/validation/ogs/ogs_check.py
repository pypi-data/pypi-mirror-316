#!/usr/bin/env python

# Check that an OGS GFF file is ready for release

import argparse
import logging
import os
import sys

from BCBio import GFF

from Bio.SeqFeature import FeatureLocation, SeqFeature


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def change_parentname(feature, parentKeyName, parentName):

    for child in feature.sub_features:
        child.qualifiers[parentKeyName][0] = parentName

    return


class OgsCheck():

    def __init__(self, source=None, no_size=False, adopt_rna_suffix="-R", rna_prefix="", exons_are_cds=False, extend_parent=False):
        self.mRNA_ids = []
        self.exon_ids = []
        self.total_exon_ids = set()
        self.total_cds_ids = set()
        self.skipped_types = set()
        self.qlistName = ['Name', 'ID']
        self.source = source
        self.no_size = no_size
        self.adopt_rna_suffix = adopt_rna_suffix
        self.rna_prefix = rna_prefix
        self.exons_are_cds = exons_are_cds
        self.extend_parent = extend_parent
        # Error management for tests. Checking logger cache does not work (shared cache between tests)
        self.has_error = False
        self.has_exotic = False

        self.current_strand = None

    def check_excluded(self, child, parent, force_error=False):
        if child.location.start < parent.location.start or child.location.start > parent.location.end or \
           child.location.end < parent.location.start or child.location.end > parent.location.end:
            if 'ID' in child.qualifiers:
                temp_id = child.qualifiers['ID']
            elif 'ID' in parent.qualifiers:
                temp_id = parent.qualifiers['ID']
            else:
                temp_id = "{}-{}".format(child.location.start, child.location.end)
            if (not self.extend_parent or force_error):
                log.error("{} {} is misplaced".format(child.type, temp_id))
                self.has_error = True
            else:
                log.warning("{} {} is misplaced. Will extend containing parent".format(child.type, temp_id))
            return True
        return False

    def extend_parent_with_child(self, child, parent):
        start = parent.location.start
        end = parent.location.end

        # Are all cases managed by this?
        if child.location.start < parent.location.start:
            start = child.location.start
            log.warning("Extending parent start to {}".format(start))
        if child.location.end > parent.location.end:
            end = child.location.end
            log.warning("Extending parent end to {}".format(end))

        return start, end

    def guess_exons_from_cds_utr(self, mrna):

        exon_coords = []  # List of exons

        for gchild in mrna.sub_features:  # exons, cds, utr

            if gchild.type in ['five_prime_UTR', 'CDS', 'three_prime_UTR']:
                exon_coords.append({'start': gchild.location.start, 'end': gchild.location.end})

        merged_exon_coords = []
        previous_exon = None
        exon_coords = sorted(exon_coords, key=lambda d: d['start'])
        for exon in exon_coords:
            if previous_exon is not None and exon['start'] == previous_exon['end']:
                merged_exon_coords[-1]['end'] = exon['end']
            else:
                merged_exon_coords.append(exon)
            previous_exon = exon

        count_id = 1
        for exon in merged_exon_coords:
            new_subf = SeqFeature(FeatureLocation(exon['start'], exon['end']), type="exon", strand=mrna.location.strand, qualifiers={"source": mrna.qualifiers['source'][0], 'ID': mrna.qualifiers['ID'][0] + "_exon" + str(count_id)})
            new_subf.qualifiers['Parent'] = mrna.qualifiers['ID']
            mrna.sub_features.append(new_subf)
            count_id += 1

        return mrna

    def create_cds_from_exons(self, mrna):

        for gchild in mrna.sub_features:  # exons, cds, utr

            if gchild.type == 'exon':

                new_subf = SeqFeature(FeatureLocation(gchild.location.start, gchild.location.end), type="CDS", strand=mrna.location.strand, qualifiers={"source": mrna.qualifiers['source'][0], 'ID': mrna.qualifiers['ID'][0] + "_cds"})
                new_subf.qualifiers['Parent'] = mrna.qualifiers['ID']
                mrna.sub_features.append(new_subf)

        return mrna

    def check_valid_mrna(self, mrna, is_complete=True):

        if mrna.type == 'transcript':
            mrna.type = "mRNA"

        if mrna.type != 'mRNA':
            log.error("Found an unexpected feature type (expected mRNA): type={} id={}".format(mrna.type, mrna.qualifiers['ID']))
            self.skipped_types.add(mrna.type)
            self.has_error = True
            return None

        if 'ID' not in mrna.qualifiers or len(mrna.qualifiers['ID']) == 0:
            log.error("Found an mRNA without an ID attribute")
            self.has_error = True
            return None

        if len(mrna.qualifiers['ID']) != 1:
            log.error("Found an mRNA with too many ID attributes ({})".format(mrna.qualifiers['ID']))
            self.has_error = True
            return None

        if mrna.qualifiers['ID'][0] in self.mRNA_ids:
            log.error("Duplicate mRNA id: %s" % mrna.qualifiers['ID'][0])
            self.has_error = True
            return None

        if 'Name' not in mrna.qualifiers or not mrna.qualifiers['Name']:
            mrna.qualifiers['Name'] = mrna.qualifiers['ID']

        if mrna.location.strand != self.current_strand:
            log.error("Strand error: %s is not on the same strand as parent entity" % mrna.qualifiers['ID'][0])
            self.has_error = True
            return None

        if is_complete:
            self.mRNA_ids.append(mrna.qualifiers['ID'][0])

        exon_coords = {}
        cds_cumul = 0
        cds_min = None
        cds_max = None

        # Find positions
        kept_gchild = []
        self.exon_ids = []
        local_cds_ids = set()

        if self.exons_are_cds:
            mrna = self.create_cds_from_exons(mrna)

        # Find all CDS positions first (need this for UTR type guessing)
        for gchild in mrna.sub_features:

            if gchild.type == "CDS":
                if cds_min is None or gchild.location.start < cds_min:
                    cds_min = gchild.location.start
                if cds_max is None or gchild.location.end > cds_max:
                    cds_max = gchild.location.end

        for gchild in mrna.sub_features:  # exons, cds, utr
            if gchild.location.strand != self.current_strand:
                log.error("Strand error: %s has a subentity on a different strand than its parent" % mrna.qualifiers['ID'][0])
                self.has_error = True
                return None

            skip = False

            if self.source:
                gchild.qualifiers['source'][0] = self.source

            if gchild.type == "exon":
                exon_coords[gchild.location.start] = gchild.location.end
            elif gchild.type == "CDS":
                cds_cumul += gchild.location.end - gchild.location.start - 1

            if gchild.type in ['five_prime_utr', "5'UTR"]:
                gchild.type = 'five_prime_UTR'

            elif gchild.type in ['three_prime_utr', "3'UTR"]:
                gchild.type = 'three_prime_UTR'

            elif gchild.type == "UTR":

                if cds_min is None or cds_max is None:
                    log.error("Found an mRNA with UTR but without any CDS ({})".format(mrna.qualifiers['ID'][0]))
                    self.has_error = True
                    return None

                if gchild.location.strand == 1:
                    if (gchild.location.start <= cds_min and  # noqa W504
                       gchild.location.end <= cds_min) or cds_min is None or cds_max is None:
                        gchild.type = 'five_prime_UTR'

                    elif gchild.location.start >= cds_max and gchild.location.end >= cds_max:
                        gchild.type = 'three_prime_UTR'
                else:
                    if (gchild.location.start <= cds_min and  # noqa W504
                       gchild.location.end <= cds_min) or cds_min is None or cds_max is None:
                        gchild.type = 'three_prime_UTR'

                    elif gchild.location.start >= cds_max and gchild.location.end >= cds_max:
                        gchild.type = 'five_prime_UTR'

            # UTR case is already managed above
            if gchild.type in ['exon', 'CDS', 'five_prime_UTR', 'three_prime_UTR']:
                if self.check_excluded(gchild, mrna):
                    if self.extend_parent:
                        new_start, new_end = self.extend_parent_with_child(gchild, mrna)
                        mrna.location = FeatureLocation(new_start, new_end, mrna.location.strand, mrna.location.ref, mrna.location.ref_db)
                    else:
                        skip = True
            # We skip this entity, we cannot manage it
            if skip:
                continue

            if gchild.type in ['exon', 'CDS', 'five_prime_UTR', 'three_prime_UTR', 'non_canonical_five_prime_splice_site', 'non_canonical_three_prime_splice_site']:
                kept_gchild.append(gchild)
            else:
                self.skipped_types.add(gchild.type)

            if gchild.type == "exon":
                if 'ID' not in gchild.qualifiers or len(gchild.qualifiers['ID']) == 0:
                    log.error("Found an exon without an ID attribute ({}-{})".format(gchild.location.start, gchild.location.end))
                    self.has_error = True
                    return None

                if len(gchild.qualifiers['ID']) != 1:
                    log.error("Found an exon with too many ID attributes ({})".format(gchild.qualifiers['ID']))
                    self.has_error = True
                    return None

                if gchild.qualifiers['ID'][0] in self.total_exon_ids:
                    log.error("Duplicate exon id: %s" % gchild.qualifiers['ID'][0])
                    self.has_error = True
                    return None

                self.total_exon_ids.add(gchild.qualifiers['ID'][0])
                self.exon_ids.append(gchild.qualifiers['ID'][0])

            elif gchild.type == "cds":
                if len(gchild.qualifiers['ID']) != 1:
                    log.error("Found a CDS with too many ID attributes ({})".format(gchild.qualifiers['ID']))
                    self.has_error = True
                    return None

                if gchild.qualifiers['ID'][0] in self.total_cds_ids:
                    log.error("Duplicate CDS id among separate genes: %s" % gchild.qualifiers['ID'][0])
                    self.has_error = True
                    return None

                local_cds_ids.add(gchild.qualifiers['ID'][0])

        mrna.sub_features = kept_gchild

        if cds_cumul > 0 and len(self.exon_ids) == 0:
            # No exon features, create them
            mrna = self.guess_exons_from_cds_utr(mrna)

        # Only check CDS/intron sizes when we're sure the mrna is complete
        if is_complete and not self.no_size:
            # Check minimum intron size
            start_sorted = sorted(exon_coords)
            previous_end = None
            for exon_start in start_sorted:
                if previous_end is not None:
                    intron_size = exon_start - previous_end
                    if intron_size < 9:
                        log.warning("Discarding '%s' because intron size %s < 9" % (mrna.qualifiers['ID'][0], intron_size))
                        return None

                previous_end = exon_coords[exon_start]

            # Check minimum cds size
            if cds_cumul < 18:
                log.warning("Discarding '%s' because CDS size < 18 (%s)" % (mrna.qualifiers['ID'][0], cds_cumul))
                return None

        if self.source:
            mrna.qualifiers['source'][0] = self.source

        # Add local cds to global set
        self.total_cds_ids |= local_cds_ids

        return mrna

    def find_inferred_parents(self, features):
        inferred = {}
        for topfeat in features:
            if topfeat.type == 'inferred_parent':
                inferred[topfeat.qualifiers['ID'][0]] = topfeat

        return inferred

    def create_parent(self, orphan, parent_id, orphan_id, parent_type):
        q = {}
        for key in orphan.qualifiers:
            q[key] = list(orphan.qualifiers[key])
        new_parent = SeqFeature(FeatureLocation(orphan.location.start, orphan.location.end), type=parent_type, strand=orphan.location.strand, qualifiers=q)
        for qn in self.qlistName:
            if qn in new_parent.qualifiers:
                new_parent.qualifiers[qn][0] = parent_id
        for qn in self.qlistName:
            if qn in orphan.qualifiers:
                # The new panret is assigned the id from the orphan, and the orphan id might be modified
                orphan.qualifiers[qn][0] = orphan_id
        new_parent.sub_features = []
        new_parent.sub_features.append(orphan)
        orphan.qualifiers['Parent'] = new_parent.qualifiers['ID']
        if 'Parent' in new_parent.qualifiers:
            del new_parent.qualifiers['Parent']
        change_parentname(orphan, 'Parent', orphan.qualifiers['ID'][0])

        if self.source:
            new_parent.qualifiers['source'][0] = self.source

        return new_parent

    def adopt_orphan_mrna(self, orphan, is_complete=True):
        # Validate it, create a gene parent, and look if we have a corresponding inferred_parent containing children from this mRNA
        if 'Parent' in orphan.qualifiers and len(orphan.qualifiers['Parent']) == 1:
            parent_id = orphan.qualifiers['Parent'][0]
            orphan_id = orphan.qualifiers['ID'][0]
        elif self.rna_prefix:
            parent_id = orphan.qualifiers["ID"][0].replace(self.rna_prefix, "")
            orphan_id = self.rna_prefix + parent_id + self.adopt_rna_suffix
        else:
            parent_id = orphan.qualifiers["ID"][0]
            orphan_id = parent_id + self.adopt_rna_suffix

        if 'ID' in orphan.qualifiers and len(orphan.qualifiers['ID']) == 1:
            if len(orphan.sub_features) == 0 and orphan.qualifiers['ID'][0] in self.inferred_parents:
                orphan.sub_features = self.inferred_parents[orphan.qualifiers['ID'][0]].sub_features
                del self.inferred_parents[orphan.qualifiers['ID'][0]]

        orphan = self.check_valid_mrna(orphan, is_complete)

        if orphan is not None:

            if parent_id in self.new_genes:
                potential_parent = self.new_genes[parent_id]

                if potential_parent.location.strand != orphan.location.strand:
                    log.error("Conflict between an orphan %s and its potential parent %s strand: %s != %s" % (orphan.type, parent_id, orphan.location.strand, potential_parent.location.strand))
                    self.has_error = True
                    return None

                potential_parent.sub_features.append(orphan)

                if potential_parent.location.start > orphan.location.start:
                    potential_parent.location = FeatureLocation(orphan.location.start, potential_parent.location.end, strand=potential_parent.location.strand)

                if potential_parent.location.end < orphan.location.end:
                    potential_parent.location = FeatureLocation(potential_parent.location.start, orphan.location.end, strand=potential_parent.location.strand)

                self.new_genes[parent_id] = potential_parent

            else:
                new_g = self.create_parent(orphan, parent_id, orphan_id, 'gene')
                self.new_genes[parent_id] = new_g

            self.all_mrnas[orphan.qualifiers['ID'][0]] = orphan

        return orphan

    def adopt_orphan_exoncds(self, orphan, last_one=True):
        # Validate it, create a gene parent, and look if we have a corresponding inferred_parent containing children from this mRNA
        if 'Parent' in orphan.qualifiers and len(orphan.qualifiers['Parent']) == 1:
            parent_id = orphan.qualifiers['Parent'][0]
            orphan_id = orphan.qualifiers['ID'][0]
        else:
            parent_id = orphan.qualifiers['ID'][0]
            orphan_id = '%s-%s' % (parent_id, orphan.type)

        if 'ID' in orphan.qualifiers and len(orphan.qualifiers['ID']) == 1:
            if len(orphan.sub_features) == 0 and orphan.qualifiers['ID'][0] in self.inferred_parents:
                orphan.sub_features = self.inferred_parents[orphan.qualifiers['ID'][0]].sub_features
                del self.inferred_parents[orphan.qualifiers['ID'][0]]

        if parent_id in self.all_mrnas:
            potential_parent = self.all_mrnas[parent_id]

            if potential_parent.location.strand != orphan.location.strand:
                log.error("Conflict between an orphan %s and its potential parent %s strand: %s != %s" % (orphan.type, parent_id, orphan.location.strand, potential_parent.location.strand))
                self.has_error = True
                return None

            del orphan.qualifiers['Parent']  # previous parent is no longer parent
            potential_parent.sub_features.append(orphan)

            if potential_parent.location.start > orphan.location.start:
                potential_parent.location = FeatureLocation(orphan.location.start, potential_parent.location.end, strand=potential_parent.location.strand)

            if potential_parent.location.end < orphan.location.end:
                potential_parent.location = FeatureLocation(potential_parent.location.start, orphan.location.end, strand=potential_parent.location.strand)

            potential_parent = self.check_valid_mrna(potential_parent, last_one)

            if potential_parent is None:
                # Failed validation => remove it from list of mrnas, and of genes
                gene_id = self.all_mrnas[parent_id].qualifiers['Parent'][0]
                gene = self.new_genes[gene_id]
                if len(gene.sub_features) == 1:
                    del self.new_genes[gene_id]
                else:
                    newsubfeats = []
                    for subfeat in gene.sub_features:
                        if subfeat.qualifiers['ID'][0] != parent_id:
                            newsubfeats.append(subfeat)
                    self.new_genes[gene_id].sub_features = newsubfeats
                del self.all_mrnas[parent_id]
                return None

            self.all_mrnas[parent_id] = potential_parent

            # update its gene parent
            gene_children = []
            for mrna in self.new_genes[potential_parent.qualifiers['Parent'][0]].sub_features:
                if mrna.qualifiers['ID'][0] == parent_id:
                    gene_children.append(potential_parent)
                else:
                    gene_children.append(mrna)
            self.new_genes[potential_parent.qualifiers['Parent'][0]].sub_features = gene_children

            # Fix gene location
            if self.new_genes[potential_parent.qualifiers['Parent'][0]].location.start > potential_parent.location.start:
                self.new_genes[potential_parent.qualifiers['Parent'][0]].location = FeatureLocation(potential_parent.location.start, self.new_genes[potential_parent.qualifiers['Parent'][0]].location.end, strand=potential_parent.location.strand)
            if self.new_genes[potential_parent.qualifiers['Parent'][0]].location.end < potential_parent.location.end:
                self.new_genes[potential_parent.qualifiers['Parent'][0]].location = FeatureLocation(self.new_genes[potential_parent.qualifiers['Parent'][0]].location.start, potential_parent.location.end, strand=potential_parent.location.strand)

        else:
            new_mRNA = self.create_parent(orphan, parent_id, orphan_id, "mRNA")
            self.all_mrnas[parent_id] = new_mRNA

            self.adopt_orphan_mrna(new_mRNA, is_complete=last_one)

        return orphan

    def is_exotic(self, entity):
        if entity.type in ['mRNA', 'transcript']:
            return entity.qualifiers.get("gbkey", []) == ["misc_RNA"]
        # All other cases are errors, they will be managed later
        return True

    def check(self, gff, genome_fa, out_gff):

        fasta_content = set()

        with open(genome_fa, 'r') as f:
            for line in f:
                if line.startswith(">"):
                    fasta_content.add(line.split(" ")[0].strip().lstrip(">"))

        scaffs = []

        for scaff in GFF.parse(gff):

            if scaff.id not in fasta_content:
                log.error("{} is not in related fasta file".format(scaff.id))
                self.has_error = True

            scaff.annotations = {}
            scaff.seq = ""

            # Genes and mRNA list, reset on each new scaff
            self.new_genes = {}
            self.all_mrnas = {}

            # First check if we have inferred_parent (generated by bcbio-gff)
            self.inferred_parents = self.find_inferred_parents(scaff.features)

            for topfeat in scaff.features:

                if topfeat.type not in ['gene', 'mRNA', 'CDS', 'exon']:
                    if topfeat.type == 'inferred_parent':
                        continue
                    else:
                        self.skipped_types.add(topfeat.type)

                if 'ID' not in topfeat.qualifiers or len(topfeat.qualifiers['ID']) == 0:
                    log.error("Found a top level %s feature without an ID attribute (%s-%s)" % (topfeat.type, topfeat.location.start, topfeat.location.end))
                    self.has_error = True
                    continue

                if len(topfeat.qualifiers['ID']) != 1:
                    log.error("Found a top level %s feature with too many ID attributes (%s)" % (topfeat.type, topfeat.qualifiers['ID']))
                    self.has_error = True
                    continue

                if topfeat.qualifiers['ID'][0] in self.new_genes.keys():
                    log.error("Duplicate top level %s feature id: %s" % (topfeat.qualifiers['ID'][0], topfeat.type))
                    self.has_error = True
                    continue

                self.current_strand = topfeat.location.strand

                if topfeat.type == 'gene':
                    # Simple case: a gene with sub features
                    new_mrnas = []

                    for mrna in topfeat.sub_features:

                        if self.is_exotic(mrna):
                            # This entity is exotic, skip it for now
                            self.has_exotic = True
                            continue

                        mrna = self.check_valid_mrna(mrna)

                        if mrna is not None:
                            new_mrnas.append(mrna)
                            self.all_mrnas[mrna.qualifiers['ID'][0]] = mrna

                    if len(new_mrnas) == 0:
                        # No more mRNA, discard gene
                        continue

                    topfeat.sub_features = new_mrnas

                    if self.source:
                        topfeat.qualifiers['source'][0] = self.source

                    if 'Name' not in topfeat.qualifiers or not topfeat.qualifiers['Name']:
                        topfeat.qualifiers['Name'] = topfeat.qualifiers['ID']

                    self.new_genes[topfeat.qualifiers['ID'][0]] = topfeat

                elif topfeat.type == 'mRNA':
                    # Found an mRNA without gene parent
                    if self.is_exotic(topfeat):
                        # This entity is exotic, skip it for now
                        self.has_exotic = True
                        continue
                    self.adopt_orphan_mrna(topfeat)
                else:
                    # This is an exotic: manage them later
                    self.has_exotic = True
                    continue

            # Now handle the remaining inferred_parents
            for topfeat_name in self.inferred_parents:
                topfeat = self.inferred_parents[topfeat_name]

                self.current_strand = topfeat.location.strand

                if len(topfeat.sub_features) < 1:
                    log.error("Skipping an inferred_parent without children %s" % topfeat)
                    self.has_error = True
                    continue

                guessed_type = None
                if topfeat.sub_features[0].type in ['exon', 'CDS', 'start_codon', 'stop_codon', 'UTR', "5'UTR", 'five_prime_UTR', 'five_prime_utr', "3'UTR", 'three_prime_UTR', 'three_prime_utr']:
                    guessed_type = 'mRNA'
                elif topfeat.sub_features[0].type == 'mRNA':
                    guessed_type = 'gene'
                else:
                    log.error("Skipping an inferred_parent: failed to guess type %s" % topfeat)
                    self.has_error = True
                    continue

                if guessed_type == 'mRNA':
                    num_seen = 0
                    for sub in topfeat.sub_features:
                        num_seen += 1
                        last_one = num_seen == len(topfeat.sub_features)
                        self.adopt_orphan_exoncds(sub, last_one=last_one)

                elif guessed_type == 'gene':
                    for sub in topfeat.sub_features:
                        self.adopt_orphan_mrna(sub)
                else:
                    log.error('Unexpected feature type %s. There is a bug.' % topfeat.type)
                    self.has_error = True

            scaff.features = self.new_genes.values()

            if len(self.new_genes):
                scaffs.append(scaff)

        if self.skipped_types:
            log.warning("Skipped unknown/misplaced feature types: %s: will be considered as exotic" % (self.skipped_types))

        with open(out_gff, 'w') as f:
            GFF.write(scaffs, f)

        return self.has_error, self.has_exotic

    def check_exotics(self, gff, genome_fa, out_gff):

        fasta_content = set()

        with open(genome_fa, 'r') as f:
            for line in f:
                if line.startswith(">"):
                    fasta_content.add(line.split(" ")[0].strip().lstrip(">"))

        scaffs = []

        for scaff in GFF.parse(gff):

            if scaff.id not in fasta_content:
                log.error("{} is not in related fasta file".format(scaff.id))
                continue
                self.has_error = True

            scaff.annotations = {}
            scaff.seq = ""

            # Genes and mRNA list, reset on each new scaff
            self.new_genes = []
            self.all_mrnas = {}

            # First check if we have inferred_parent (generated by bcbio-gff)
            self.inferred_parents = self.find_inferred_parents(scaff.features)

            for topfeat in scaff.features:

                if topfeat.type == "gene":
                    # Simple case: a gene with sub features
                    new_mrnas = []

                    for mrna in topfeat.sub_features:

                        if not self.is_exotic(mrna):
                            continue

                        new_mrnas.append(mrna)
                        self.all_mrnas[mrna.qualifiers['ID'][0]] = mrna

                    if len(new_mrnas) == 0:
                        # No more mRNA, discard gene
                        continue

                    topfeat.sub_features = new_mrnas

                elif topfeat.type == "mRNA":
                    # This entity is not exotic, skip it
                    if not self.is_exotic(topfeat):
                        continue

                if topfeat.type == 'inferred_parent':
                    # Ignore stuff inferred by the reader, we want the content as-is
                    continue

                # Do we need this?
                if self.source:
                    topfeat.qualifiers['source'][0] = self.source

                # Do we need this?
                if 'Name' not in topfeat.qualifiers or not topfeat.qualifiers['Name']:
                    topfeat.qualifiers['Name'] = topfeat.qualifiers['ID']

                self.new_genes.append(topfeat)

            scaff.features = self.new_genes

            if len(self.new_genes):
                scaffs.append(scaff)

        with open(out_gff, 'w') as f:
            GFF.write(scaffs, f)

        return self.has_error


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str, help="Input GFF")
    parser.add_argument('genome', type=str, help="Genome sequence (fasta format)")
    parser.add_argument('dest', type=str, help="Output GFF")
    parser.add_argument('--source', help="Change the source to given value for all features")
    parser.add_argument('--no-size', action='store_true', help="Disable CDS and intron size checking")
    parser.add_argument('--adopt-rna-suffix', help="Suffix to be appended to orphan mRNA ids when adopted by newly created genes", default="-R")
    parser.add_argument('--exons-are-cds', action='store_true', help="Consider that exons represent CDS (when cds are absent and exons are present)")
    parser.add_argument("--rna-prefix", type=str, help="mRNA prefix to add to mRNAs and subfeatures", default="")
    parser.add_argument('--extend-parent', action='store_true', help="Extend mRNA if subentities are outside of it")
    args = parser.parse_args()

    log.info("Checking %s (with genome %s), will write fixed GFF to %s" % (args.infile, args.genome, args.dest))
    ogsc = OgsCheck(args.source, args.no_size, args.adopt_rna_suffix, args.rna_prefix, args.exons_are_cds, args.extend_parent)
    has_error, has_exotic = ogsc.check(args.infile, args.genome, args.dest)
    if not has_error and has_exotic:
        log.info("Exotic entities found. Writing separate file")
        path, ext = os.path.splitext(args.dest)
        new_output = '{}_exotic{}'.format(path, ext)
        # Create new object to clear various caches
        ogsc = OgsCheck(args.source, args.no_size, args.adopt_rna_suffix, args.rna_prefix, args.exons_are_cds, args.extend_parent)
        ogsc.check_exotics(args.infile, args.genome, new_output)

    # Raise an error if there were some logged
    if 40 in log._cache and log._cache[40]:
        sys.exit(1)
