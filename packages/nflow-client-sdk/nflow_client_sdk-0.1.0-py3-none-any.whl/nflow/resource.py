import asyncio

class Resource:
    def __init__(self, name, collection, type, format):
        self.name = name
        self.collection = collection
        self.type = type
        self.format = format
        self.progress = 0
        self.id = f"{name}-{collection}"

    async def upload_async(self, path, progress_callback=None):
        print(f"Uploading resource '{self.name}' from {path}...")
        total_size = 100
        chunk_size = 10

        for i in range(0, total_size, chunk_size):
            await asyncio.sleep(0.5)
            self.progress = (i + chunk_size) / total_size * 100
            if progress_callback:
                progress_callback(self.progress)

        self.progress = 100
        if progress_callback:
            progress_callback(self.progress)
        print(f"Upload of resource '{self.name}' complete!")

    async def download_async(self, path, progress_callback=None):
        print(f"Downloading resource '{self.name}' to {path}...")
        total_size = 100
        chunk_size = 10

        for i in range(0, total_size, chunk_size):
            await asyncio.sleep(0.5)
            self.progress = (i + chunk_size) / total_size * 100
            if progress_callback:
                progress_callback(self.progress)

        self.progress = 100
        if progress_callback:
            progress_callback(self.progress)
        print(f"Download of resource '{self.name}' complete!")
