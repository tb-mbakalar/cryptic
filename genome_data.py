import torch
import re
import genomepy.seq
import torch.nn.functional as F

class DinucleotideDataset(torch.utils.data.IterableDataset):
    
    translation_dict = {"A":0,"C":1,"T":2,"G":3,"N":4}

    def __init__(self, data_file, dinucleotide, length):
        self.genome = genomepy.seq.as_seqdict(data_file)
        self.dinucleotide = dinucleotide
        self.length = length

    def one_hot(self, sequence):
        encoding = torch.tensor([self.translation_dict[c] for c in sequence.upper()])
        x = F.one_hot(encoding, num_classes=len(self.translation_dict)).to(torch.float32)
        return x

    def __iter__(self):
        for chr in self.genome.keys():
            genomic_sequence = self.genome[chr].upper()
            pattern = re.compile(r"({})".format(self.dinucleotide))
            for m in pattern.finditer(genomic_sequence):
                window = int((self.length-2)/2)
                start = m.span()[0] - window
                end = m.span()[1] + window
                sequence = genomic_sequence[start:end]
                if len(sequence) == self.length:
                    yield(chr, start, end, sequence, self.one_hot(sequence))

if __name__ == "__main__":
    dataset = DinucleotideDataset('../data/reference/hg38.fa','GT', length=50)
    # Print first 10 sequences
    for i, item in enumerate(dataset):
        print(item[0],item[3])