import math

def cohen_d_from_lists(group1, group2):
    """Compute Cohen's d for independent samples using lists of measurements."""
    mean1, mean2 = sum(group1) / len(group1), sum(group2) / len(group2)
    sd1 = math.sqrt(sum([(x - mean1) ** 2 for x in group1]) / (len(group1) - 1))
    sd2 = math.sqrt(sum([(x - mean2) ** 2 for x in group2]) / (len(group2) - 1))
    n1, n2 = len(group1), len(group2)

    # Compute the pooled standard deviation
    pooled_sd = math.sqrt(((n1 - 1) * sd1 ** 2 + (n2 - 1) * sd2 ** 2) / (n1 + n2 - 2))

    # Compute Cohen's d
    d = (mean1 - mean2) / pooled_sd
    return d
