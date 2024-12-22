class DataPipeline:
    """A simple data processing pipeline class."""

    def __init__(self):
        self.steps = []

    def add_step(self, func):
        """Add a processing step to the pipeline.

        Args:
            func (callable): The processing function to add.
        """
        self.steps.append(func)

    def run(self, data):
        """Run the pipeline on the given data.

        Args:
            data: The input data to process.

        Returns:
            Processed data after all steps are applied.
        """
        for step in self.steps:
            data = step(data)
        return data
