from .client import Client

class System:

    def __init__(self, client: Client):
        self.client = client

    def system_info(self):
        """
        Get the system information
        """
        return self.client.get("GetSession")
    
    def set_system_info(self, name=None, email=None, organization=None, contact_name=None, phones=None, invoice_name=None, invoice_address=None, fax=None, access_password=None, record_password=None):
        """
        Set the system information
        """
        data = {
            "name": name,
            "email": email,
            "organization": organization,
            "contactName": contact_name,
            "phones": phones,
            "invoiceName": invoice_name,
            "invoiceAddress": invoice_address,
            "fax": fax,
            "accessPassword": access_password,
            "recordPassword": record_password
        }
        return self.client.post("SetCustomerDetails", data)
    
    def set_password(self, new_password):
        """
        Set the password
        """
        if not isinstance(new_password, int):
            return "The password must be a integer"
        new = self.client.get("SetPassword", {"password": self.client.password, "newPassword": new_password})
        self.client.password = new_password
        return new
    
    def get_transactions(self, first=None, limit='100', filter=None):
        """
        Get the units transactions, you can filter by the filter parameter (optional)  for example: "campaigns"
        """
        return self.client.get("GetTransactions", {"first": first, "limit": limit})
    
    def transfer_units(self, amount, destination):
        """
        Transfer units
        """
        if not isinstance(amount, int):
            return "The amount must be a integer"
        if not isinstance(destination, int):
            return "The destination must be a integer"
        return self.client.get("TransferUnits", {"amount": amount, "destination": destination})
    
    def get_incoming_calls(self):
        """
        Get the incoming calls
        """
        return self.client.get("GetIncomingCalls")
    
    def upload_file(self, file=None, path=None, convert_audio=0, auto_numbering=False, tts=0):
        """
        Upload file this is for uploading a file what is ander 50MB for bigger files use the upload_file_big
        """
        if not file:
            return "The file is required"
        # check if the path starts with ivr2:
        if path and not path.startswith("ivr2:"):
            return "The path must start with ivr2:"
        if convert_audio not in [0, 1]:
            return "The convert_audio must be 0 or 1"
        if tts not in [0, 1]:
            return "The tts must be 0 or 1"
        if auto_numbering not in [True, False]:
            return "The auto_numbering must be True or False"
        
        data = {
            "path": path,
            "convertAudio": convert_audio,
            "autoNumbering": auto_numbering,
            "tts": tts
        }
        files = {}
        if file:
            files["file"] = open(file, "rb")
        return self.client.post("UploadFile", data=data, files=files)
    
    def upload_file_big(self, file=None, path=None, convert_audio=None, auto_numbering=None, tts=None):
        """
        Upload file this is for uploading a file what is over 50MB
        """
        # TODO: Implement this method

        # split the file to parts and upload each part in the first part generate a qquuid and send it to the server
        # the parameter what i need to send in each part is 
        # qquuid - the generated qquuid
        # qqpartindex - the part index
        # qqpartbyteoffset - the part byte offset
        # qqchunksize - the chunk size
        # qqtotalparts - the total parts
        # qqtotalfilesize - the total file size in bytes
        # qqfilename - the file name
        # qqfile - the file
        # uploader - yemot-admin
        return "Not implemented"
    
    def download_file(self, path):
        """
        Download file
        """
        if not path:
            return "The path is required"
        return self.client.get("DownloadFile", {"path": path})   