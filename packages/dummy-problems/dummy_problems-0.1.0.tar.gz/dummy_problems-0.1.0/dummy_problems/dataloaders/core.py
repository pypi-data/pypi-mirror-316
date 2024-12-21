from torch.utils.data import Dataset, DataLoader


class BaseDataset(Dataset, ABC):
    def __init__(self, settings)