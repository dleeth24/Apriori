import pandas as pd

df = pd.read_csv('Groceries_dataset.csv')

transactions = df.groupby(['Member_number', 'Date'])['itemDescription'].apply(list).tolist()

print(f"Total transactions: {len(transactions)}")

def create_initial_set(transactions):
    c1 = []
    for transaction in transactions:
        for item in transaction:
            if [item] not in c1:
                c1.append([item])
    c1.sort()
    return list(map(frozenset, c1))

c1 = create_initial_set(transactions)

def scan_transactions(transactions, candidates, min_support):
    """ Calculates the support for items in the candidate list
    and returns a subset of the candidate list
    that meets the minimum support level. """
    item_count = {}
    for transaction in transactions:
        for candidate in candidates:
            if candidate.issubset(transaction):
                item_count.setdefault(candidate, 0)
                item_count[candidate] += 1

    num_transactions = len(transactions)
    frequent_items = []
    support_data = {}
    for item in item_count:
        support = item_count[item] / num_transactions
        if support >= min_support:
            frequent_items.insert(0, item)
        support_data[item] = support
    return frequent_items, support_data

def apriori_gen(freq_sets, k):
    """
    Generate the joint transactions from candidate sets in Lk-1.
    """
    ret_list = []
    len_freq_sets = len(freq_sets)
    for i in range(len_freq_sets):
        for j in range(i+1, len_freq_sets):
            L1 = list(freq_sets[i])[:k-2]
            L2 = list(freq_sets[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                ret_list.append(freq_sets[i] | freq_sets[j])
    return ret_list

def apriori(transactions, min_support):
    """
    The main apriori algorithm. Returns all frequent itemsets.
    """
    C1 = create_initial_set(transactions)
    D = list(map(set, transactions))
    L1, support_data = scan_transactions(D, C1, min_support)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
        Ck = apriori_gen(L[k-2], k)
        Lk, supK = scan_transactions(D, Ck, min_support)
        support_data.update(supK)
        L.append(Lk)
        k += 1
    return L, support_data

def generate_rules(L, support_data, min_confidence=0.002, min_lift=3, min_length=2, max_length=2):
    big_rule_list = []
    for i in range(1, len(L)):  # Only get the sets with two or more items
        for freq_set in L[i]:
            if len(freq_set) > max_length or len(freq_set) < min_length:
                continue  # Skip the current loop if the itemset size is out of desired range
            H1 = [frozenset([item]) for item in freq_set]
            if (i > 1):
                rules_from_conseq(freq_set, H1, support_data, big_rule_list, min_confidence)
            else:
                calc_confidence(freq_set, H1, support_data, big_rule_list, min_confidence, min_lift)
    return big_rule_list


def calc_confidence(freq_set, H, support_data, rules, min_confidence, min_lift=1):
    pruned_H = []
    for conseq in H:
        conf = support_data[freq_set] / support_data[freq_set - conseq]
        lift = calc_lift(freq_set - conseq, conseq, support_data)
        if conf >= min_confidence and lift >= min_lift:
            rules.append((freq_set - conseq, conseq, conf, lift))
            pruned_H.append(conseq)
    return pruned_H


def calc_lift(antecedent, consequent, support_data):
    # Lift(A -> B) = Support(A ∪ B) / (Support(A) * Support(B))
    support_antecedent = support_data[antecedent]
    support_consequent = support_data[consequent]
    support_antecedent_consequent = support_data[antecedent | consequent]
    lift = support_antecedent_consequent / (support_antecedent * support_consequent)
    return lift


def rules_from_conseq(freq_set, H, support_data, rules, min_confidence):
    """
    Generate more rules from the current set by merging subsets.
    """
    m = len(H[0])
    if (len(freq_set) > (m + 1)):
        Hmp1 = apriori_gen(H, m+1)
        Hmp1 = calc_confidence(freq_set, Hmp1, support_data, rules, min_confidence)
        if (len(Hmp1) > 1):
            rules_from_conseq(freq_set, Hmp1, support_data, rules, min_confidence)

def filter_itemsets_by_length(L, min_length=2, max_length=2):
    filtered_L = []
    for level in L:
        filtered_level = [itemset for itemset in level if min_length <= len(itemset) <= max_length]
        filtered_L.append(filtered_level)
    return filtered_L


L, support_data = apriori(transactions, min_support=0.0008)

L_filtered = filter_itemsets_by_length(L, 3, 3)

rules = generate_rules(L_filtered, support_data, min_confidence=0.0008, min_lift=1, min_length=3, max_length=3)

def print_rules(rules):
    if not rules:
        print("No rules generated.")
        return
    
    for rule in rules:
        antecedent, consequent, confidence, lift = rule
        print(f"Rule: {set(antecedent)} -> {set(consequent)}, Confidence: {confidence:.3f}, Lift: {lift:.2f}")

print_rules(rules)

