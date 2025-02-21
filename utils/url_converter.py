# url_converter.py
import re

class URLConverter:
    def convert_url(self, viewer_url):
        """
        Converts a URL to a direct download URL, automatically detecting the service.
        Supports Google Drive, Dropbox, and basic OneDrive conversion.
        Returns the direct download URL if successful, otherwise None.
        """
        if "lh3.googleusercontent.com" in viewer_url:
            # Already a direct URL
            return viewer_url
        elif "drive.google.com" in viewer_url:
            return self._convert_google_drive_url(viewer_url)
        elif "dropbox.com" in viewer_url:
            return self._convert_dropbox_url(viewer_url)
        elif "onedrive.live.com" in viewer_url or "1drv.ms" in viewer_url:
            return self._convert_onedrive_url(viewer_url)
        else:
            print(f"Warning: URL service not recognized for: {viewer_url}.  Returning original URL (may not be direct download).")
            return viewer_url # Return original URL as fallback if service is not recognized

    def _convert_google_drive_url(self, viewer_url):
        """
        Converts a Google Drive viewer URL to a direct download URL. (Private method)
        """
        print(f"\nDebug - Converting Google Drive URL: {viewer_url}")
        
        # Try to find file ID in different URL formats
        file_id = None
        
        # Format 1: /d/{file_id}/
        file_id_match = re.search(r"/d/(.*?)/", viewer_url)
        if file_id_match:
            file_id = file_id_match.group(1)
            print(f"Found file ID via /d/ format: {file_id}")
        
        # Format 2: open?id={file_id}
        if not file_id:
            file_id_match = re.search(r"[?&]id=([^&]+)", viewer_url)
            if file_id_match:
                file_id = file_id_match.group(1)
                print(f"Found file ID via open?id format: {file_id}")
        
        # Format 3: /file/d/{file_id}/
        if not file_id:
            file_id_match = re.search(r"/file/d/(.*?)/", viewer_url)
            if file_id_match:
                file_id = file_id_match.group(1)
                print(f"Found file ID via /file/d/ format: {file_id}")
        
        if not file_id:
            print("Could not extract file ID from URL")
            return None
        
        # Use high-res preview URL (w=3000 for large size)
        direct_url = f"https://lh3.googleusercontent.com/d/{file_id}=w3000"
        print(f"Generated direct URL: {direct_url}")
        return direct_url

    def _convert_dropbox_url(self, viewer_url):
        """
        Converts a Dropbox share URL to a direct download URL. (Private method)
        """
        return viewer_url.replace("?dl=0", "?dl=1")

    def _convert_onedrive_url(self, viewer_url):
        """
        Placeholder for OneDrive URL conversion (needs more robust implementation). (Private method)
        """
        print("Warning: Basic OneDrive URL conversion - may not be reliable.")
        return None  # Placeholder - needs improvement