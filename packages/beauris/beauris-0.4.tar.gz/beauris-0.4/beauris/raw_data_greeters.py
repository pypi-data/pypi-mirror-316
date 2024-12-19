import gzip
import hashlib
import logging
import os
import shutil

import requests

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class RawDataGreeters():

    def __init__(self):

        # Fetch data from remote source
        self.downloaders = [
            HttpDownloader(),
            # Other potential future downloaders (not implemented yet):
            # FtpDownloader,
            # S3Downloader,
        ]

        self.post_processes = [
            HashChecker(),
            GzUnzipper(),
            AsIsMover(),
        ]

    def greet_data(self, src, dest, hash_type, hash_value, need_download=False):

        if need_download:
            temp_down = dest + ".down_tmp"
            if ".gz" in src:
                temp_down += ".gz"
            if (os.path.isdir(temp_down)):
                os.path.remove(temp_down)

            for der in self.downloaders:
                downloaded = der.process(src, temp_down)
                if downloaded:
                    log.info("File downloaded with {}".format(der.__class__.__name__))
                    break

            if not downloaded:
                raise RuntimeError("Could not download file from URL {}".format(src))

            to_post_process = temp_down
        else:
            to_post_process = src

        for pder in self.post_processes:
            pder.process(to_post_process, dest, hash_type, hash_value, need_download)


class Downloader():

    def __init__(self):
        pass

    def process(self, url, dest):
        """
        Tries to process an url, returns a path to downloaded
        """
        raise NotImplementedError()


class HttpDownloader(Downloader):

    def process(self, url, dest):
        try:
            if url.startswith("http://") or url.startswith("https://"):
                with requests.get(url, stream=True) as r:
                    r.raise_for_status()
                    with open(dest, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=10 * 1024):
                            f.write(chunk)

                return True
        except OSError as e:
            if (os.path.exists(dest)):
                os.remove(dest)
            raise Exception(f"Error downloading {url}, removing {dest}. Error: {e}")


class PostDownloader():

    def __init__(self):
        pass

    def process(self, temp, dest, was_downloaded=False):
        """
        Tries to process a downloaded (or local) file

        Return True if no other post processor should be called, False otherwise.
        Raise exceptions in case of errors
        """
        raise NotImplementedError()


class HashChecker(PostDownloader):
    def process(self, temp, dest, hash_type, hash_value, was_downloaded=False):

        if hash_type is None or hash_value is None:
            log.info(f"No checksum verification for {temp}.")
            return False

        if hash_type not in ("sha256"):
            raise Exception(f"Unsupported hash type {hash_type}")

        sha256_hash = hashlib.sha256()
        with open(temp, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
                sha256 = sha256_hash.hexdigest()

        if hash_value != sha256:
            raise Exception(f"Wrong checksum for {temp}: expected {hash_value} got {sha256}")

        return False


class GzUnzipper(PostDownloader):

    def process(self, temp, dest, hash_type, hash_value, was_downloaded=False):

        if temp.endswith(".gz"):
            with gzip.open(temp, 'rb') as f_in:
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            return True

        return False


class AsIsMover(PostDownloader):

    def process(self, temp, dest, hash_type, hash_value, was_downloaded=False):

        # Default action for download: just move
        if was_downloaded:
            if ".gz" not in temp:
                shutil.move(temp, dest)

        return True
