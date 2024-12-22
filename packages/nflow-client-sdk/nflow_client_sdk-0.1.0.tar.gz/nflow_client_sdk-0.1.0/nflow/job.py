import asyncio

class Job:
    def __init__(self, pipeline_id, trigger):
        self.pipeline_id = pipeline_id
        self.trigger = trigger
        self.id = f"job-{pipeline_id}"

    def start(self):
        print(f"Starting job '{self.id}' with trigger: {self.trigger.cron}")
        return self.id

    async def wait_for_start(self):
        print(f"Job '{self.id}' is waiting to start...")
        await asyncio.sleep(3)  # Simulate delay before job starts
        print(f"Job '{self.id}' has started!")

    async def run(self):
        await self.wait_for_start()  # Simulate waiting for job to start
        print(f"Executing pipeline for job '{self.id}'...")
        total_steps = 10  # Simulated job execution steps
        for i in range(total_steps):
            await asyncio.sleep(1)  # Simulate execution delay
            progress = (i + 1) / total_steps * 100
            print(f"Job '{self.id}' execution progress: {progress:.2f}%")
        print(f"Job '{self.id}' execution complete!")
