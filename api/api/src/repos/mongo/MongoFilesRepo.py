from .MongoRepo import MongoRepo


class MongoFilesRepo(MongoRepo):
    def __init__(self):
        super().__init__()

    def retrieve_file(self, files_id, filename, version=None):
        # query = {"name": filename}
        # if version:
        #     query["version"] = version
        # return self._retrieve(
        #     "files",
        #     {
        #         "id": files_id,
        #         "files": {"$elemMatch": query},
        #     },
        #     {"files.$": 1},
        # )
        query = [
            {"$match": {"id": files_id}},
            {"$unwind": "$files"},
            {"$match": {"files.name": filename}}
        ]
        if version:
            query.append({"$match": {"files.versions": version}})
        query.append({"$group": {"_id": "$_id", "files": {"$push": "$files"}}})
        results = list(self.db["files"].aggregate(query))
        return results[0] if results else None

    def add_file(self, files_id, file):
        return self.push("files", files_id, {"files": file})

    def update_file(self, files_id, filename, version, file):
        return self._update(
            "files",
            {
                "id": files_id,
                "files": {
                    "$elemMatch": {
                        "name": filename,
                        "version": version,
                    }
                },
            },
            {"$set": {"files.$": file}},
        )

    def add_folder_version(self, files_id, folder_name, version):
        return self._update(
            "files",
            {"id": files_id, "folders.name": folder_name},
            {"$addToSet": {"folders.$.versions": version}},
        )

    def add_folder(self, files_id, folder):
        return self.push("files", files_id, {"folders": folder})

    def retrieve_files(self, files_id, version=None):
        query = [
            {"$match": {"id": files_id}},
            {"$unwind": "$files"},
        ]
        if version:
            query.append({"$match": {"files.versions": version}})
        query.append({"$group": {"_id": "$_id", "files": {"$push": "$files"}}})
        return list(self.db["files"].aggregate(query))

    def find_upload(self, uid, filename, file_version, dataset_id):
        return self.find_one(
            "uploading",
            {
                "uid": uid,
                "filename": filename,
                "dataset": dataset_id,
                "version": file_version,
            },
        )

    def find_upload_by_id(self, uid, upload_id):
        return self.find_one(
            "uploading",
            {"uid": uid, "upload_id": upload_id},
        )

    def delete_upload(self, upload_id):
        return self.delete("uploading", upload_id)

    def persist_upload(self, upload_id, data):
        return self.persist("uploading", data, upload_id)

    def retrieve_upload(self, upload_id):
        return self.retrieve("uploading", upload_id, "upload_id")

    def update_upload(self, upload_id, data):
        return self.update("uploading", upload_id, data)
