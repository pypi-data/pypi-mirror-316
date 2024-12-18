import numpy as np
from .Gene import Gene
from .SeqMats import MutSeqMat
from collections import defaultdict
from . import config

def generate_adjacency_list(acceptors, donors, transcript_start, transcript_end, max_distance=50, rev=False):
    # Append the transcript end to donors to allow connection to the end point
    donors.append((transcript_end, 1))
    acceptors = sorted(acceptors, key=lambda x: (x[0], x[1] if not rev else -x[1]), reverse=rev)
    donors = sorted(donors, key=lambda x: (x[0], x[1] if not rev else -x[1]), reverse=rev)

    # Initialize adjacency list to store downstream connections
    adjacency_list = defaultdict(list)

    # Connect each donor to the nearest acceptor(s) within the distance threshold
    for d_pos, d_prob in donors:
        running_prob = 1
        for a_pos, a_prob in acceptors:
            correct_orientation = (a_pos > d_pos and not rev) or (a_pos < d_pos and rev)
            distance_valid = abs(a_pos - d_pos) <= max_distance
            if correct_orientation and distance_valid:
                in_between_acceptors = sum([d_pos < a < a_pos for a, _ in acceptors]) if not rev else sum([a_pos < a < d_pos for a, _ in acceptors])
                in_between_donors = sum([d_pos < d < a_pos for d, _ in donors]) if not rev else sum([a_pos < d < d_pos for d, _ in donors])
                in_between_naturals = 0
                if in_between_donors == 0 or in_between_acceptors == 0:
                    adjacency_list[(d_pos, 'donor')].append((a_pos, 'acceptor', a_prob))
                    running_prob -= a_prob

                else:
                    if running_prob > 0:
                        adjacency_list[(d_pos, 'donor')].append((a_pos, 'acceptor', a_prob*running_prob))
                        running_prob -= a_prob
                    else:
                        break

    # Connect each acceptor to the nearest donor(s) within the distance threshold
    for a_pos, a_prob in acceptors:
        running_prob = 1
        for d_pos, d_prob in donors:
            correct_orientation = (d_pos > a_pos and not rev) or (d_pos < a_pos and rev)
            distance_valid = abs(d_pos - a_pos) <= max_distance
            if correct_orientation and distance_valid:
                in_between_acceptors = sum([a_pos < a < d_pos for a, _ in acceptors]) if not rev else sum([d_pos < a < a_pos for a, _ in acceptors])
                in_between_donors = sum([a_pos < d < d_pos for d, _ in donors]) if not rev else sum([d_pos < d < a_pos for d, _ in donors])
                in_between_naturals = 0
                tag = 'donor' if d_pos != transcript_end else 'transcript_end'

                if in_between_acceptors == 0:
                    adjacency_list[(a_pos, 'acceptor')].append((d_pos, tag, d_prob))
                    running_prob -= d_prob
                else:
                    if running_prob > 0:
                        adjacency_list[(a_pos, 'acceptor')].append((d_pos, tag, d_prob*running_prob))
                        running_prob -= d_prob
                    else:
                        break

    # Connect the transcript start to the nearest donor(s) within the distance threshold
    running_prob = 1
    for d_pos, d_prob in donors:
        if ((d_pos > transcript_start and not rev) or (d_pos < transcript_start and rev)) and abs(
                d_pos - transcript_start) <= max_distance:
            adjacency_list[(transcript_start, 'transcript_start')].append((d_pos, 'donor', d_prob))
            running_prob -= d_prob
            if running_prob <= 0:
                break

    # Normalize probabilities to ensure they sum up to 1 for each list of connections
    for k, next_nodes in adjacency_list.items():
        prob_sum = sum([c for a, b, c in next_nodes])
        adjacency_list[k] = [(a, b, round(c / prob_sum, 3)) for a, b, c in next_nodes] if prob_sum > 0 else next_nodes

    return adjacency_list


def find_all_paths(graph, start, end, path=[], probability=1.0):
    path = path + [start]  # Add current node to the path
    if start == end:
        yield path, probability  # If end is reached, yield the path and its cumulative probability
        return
    if start not in graph:
        return  # If the start node has no outgoing edges, return

    for (next_node, node_type, prob) in graph[start]:
        # Recur for each connected node, updating the probability
        yield from find_all_paths(graph, (next_node, node_type), end, path, probability * prob)


def prepare_splice_sites(acceptors, donors, aberrant_splicing):
    acceptors = {p: 1 for p in acceptors}
    donors = {p: 1 for p in donors}

    for p, v in aberrant_splicing[f'missed_donors'].items():
        donors[p] = v['absolute']

    for p, v in aberrant_splicing[f'discovered_donors'].items():
        donors[p] = v['absolute']

    for p, v in aberrant_splicing[f'missed_acceptors'].items():
        acceptors[p] = v['absolute']

    for p, v in aberrant_splicing[f'discovered_acceptors'].items():
        acceptors[p] = v['absolute']

    acceptors = {int(k): v for k, v in acceptors.items()}
    donors = {int(k): v for k, v in donors.items()}
    return list(acceptors.items()), list(donors.items())


def develop_aberrant_splicing(transcript, aberrant_splicing):
    all_acceptors, all_donors = prepare_splice_sites(transcript.acceptors, transcript.donors, aberrant_splicing)
    adj_list = generate_adjacency_list(all_acceptors, all_donors, transcript_start=transcript.transcript_start,
                                       transcript_end=transcript.transcript_end, rev=transcript.rev,
                                       max_distance=100000)
    end_node = (transcript.transcript_end, 'transcript_end')
    start_node = (transcript.transcript_start, 'transcript_start')
    for path, prob in find_all_paths(adj_list, start_node, end_node):
        yield {'acceptors': [p[0] for p in path if p[1] == 'acceptor'],
               'donors': [p[0] for p in path if p[1] == 'donor'], 'path_weight': prob}



# Missplicing Detection
def find_ss_changes(ref_dct, mut_dct, known_splice_sites, threshold=0.5):
    '''
    :param ref_dct:  the spliceai probabilities for each nucleotide (by genomic position) as a dictionary for the reference sequence
    :param mut_dct:  the spliceai probabilities for each nucleotide (by genomic position) as a dictionary for the mutated sequence
    :param known_splice_sites: the indices (by genomic position) that serve as known splice sites
    :param threshold: the threshold for detection (difference between reference and mutated probabilities)
    :return: two dictionaries; discovered_pos is a dictionary containing all the positions that meat the threshold for discovery
            and deleted_pos containing all the positions that meet the threshold for missing and the condition for missing
    '''

    new_dict = {v: mut_dct.get(v, 0) - ref_dct.get(v, 0) for v in
                list(set(list(ref_dct.keys()) + list(mut_dct.keys())))}

    discovered_pos = {k: {'delta': round(float(v), 3), 'absolute': round(float(mut_dct[k]), 3), 'reference': round(ref_dct[k], 3)} for k, v in
                      new_dict.items() if v >= threshold} # and k not in known_splice_sites}   # if (k not in known_splice_sites and v >= threshold) or (v > 0.45)}

    deleted_pos = {k: {'delta': round(float(v), 3), 'absolute': round(float(mut_dct.get(k, 0)), 3), 'reference': round(ref_dct[k], 3)} for k, v in
                   new_dict.items() if -v >= threshold} # and k in known_splice_sites}      #if k in known_splice_sites and v <= -threshold}

    return discovered_pos, deleted_pos


from typing import Tuple, Dict

def run_splicing_engine(seq, engine='spliceai'):
    match engine:
        case 'spliceai':
            from .spliceai_utils import sai_predict_probs, sai_models
            donor_probs, acceptor_probs = sai_predict_probs(seq, models=sai_models)

        case 'pangolin':
            from .pangolin_utils import pangolin_predict_probs, pang_models
            donor_probs, acceptor_probs = pangolin_predict_probs(seq, models=pang_models)

        case _:
            raise ValueError(f"{engine} not implemented")
    return donor_probs, acceptor_probs


def find_transcript_splicing(transcript, engine: str = 'spliceai') -> Tuple[Dict[int, float], Dict[int, float]]:
    """
    Predict splice site probabilities for a given transcript using the specified engine.
    This function uses a padding of 5000 'N's on each side of the transcript sequence
    to align with the model's required context length.

    Args:
        transcript: An object representing a transcript, expected to have:
            - an `indices` attribute that returns a sequence of positions.
            - a `seq` attribute that returns the sequence string.
        engine (str): The prediction engine to use. Supported: 'spliceai', 'pangolin'.

    Returns:
        (donor_probs, acceptor_probs) as two dictionaries keyed by position with probability values.

    Raises:
        ValueError: If an unsupported engine is provided.
        AssertionError: If the length of predicted probabilities does not match the length of indices.
    """
    # Prepare reference sequence with padding
    ref_indices = transcript.indices
    ref_seq = 'N' * 5000 + transcript.seq + 'N' * 5000
    ref_seq_acceptor_probs, ref_seq_donor_probs = run_splicing_engine(ref_seq, engine)

    # Verify lengths
    assert len(ref_seq_donor_probs) == len(ref_indices), (
        f"Donor probabilities length ({len(ref_seq_donor_probs)}) does not match "
        f"indices length ({len(ref_indices)})."
    )
    assert len(ref_seq_acceptor_probs) == len(ref_indices), (
        f"Acceptor probabilities length ({len(ref_seq_acceptor_probs)}) does not match "
        f"indices length ({len(ref_indices)})."
    )

    # Create dictionaries and sort them by probability in descending order
    donor_probs = dict(sorted((i, p) for i, p in zip(ref_indices, ref_seq_donor_probs)),
                       key=lambda item: item[1], reverse=True)
    acceptor_probs = dict(sorted((i, p) for i, p in zip(ref_indices, ref_seq_acceptor_probs)),
                          key=lambda item: item[1], reverse=True)

    return donor_probs, acceptor_probs


def find_transcript_missplicing(mut_id, transcript=None, threshold=0.5, engine='spliceai', organism='hg38'):
    gene = Gene.from_file(mut_id.split(':')[0], organism=organism)
    reference_transcript = gene.transcript(transcript) if transcript is not None else gene.transcript()
    variant_transcript = reference_transcript.clone()
    mutations = [MutSeqMat.from_mutid(m) for m in mut_id.split('|')]
    mutations = [m for m in mutations if m in reference_transcript]
    if len(mutations) == 0:
        return {'missed_acceptors': {}, 'missed_donors': {}, 'discovered_acceptors': {}, 'discovered_donors': {}}

    center = np.mean([m.indices[0] for m in mutations]) // 1
    for mutation in mutations:
        variant_transcript.mutate(mutation, inplace=True)

    return find_transcript_missplicing_seqs(reference_transcript.pre_mrna.get_context(center, 7500), variant_transcript.pre_mrna.get_context(center, 7500), reference_transcript.donors, reference_transcript.acceptors, threshold=threshold, engine=engine)


    # from functools import reduce
    # ref = transcript.pre_mrna
    # mutations = [mutation for mutation in mutations if mutation.position in ref.indices]
    # if len(mutations) == 0:
    #     return {'missed_acceptors': {}, 'missed_donors': {}, 'discovered_acceptors': {}, 'discovered_donors': {}}
    #
    # var = reduce(lambda acc, mutation: acc + mutation, mutations, ref)
    # center = int(np.mean([mutation.position for mutation in mutations]) // 1)
    #
    # total_context = context + window
    # length = ref.seqmat.shape[-1]
    # center_index = ref.rel_pos(center)
    # ref_start_pad = max(0, total_context - center_index)
    # ref_end_pad = max(0, total_context - (length - center_index))
    #
    # length = var.seqmat.shape[-1]
    # center_index = var.rel_pos(center)
    # if center_index is None:
    #     raise IndexError("Center index must not be none... Issue with mutations... They must not be within the transcript.")
    #
    # var_start_pad = max(0, total_context - center_index)
    # var_end_pad = max(0, total_context - (length - center_index))
    #
    # ref = ref.inspect(center, context=total_context)
    # var = var.inspect(center, context=total_context)
    #
    # ref_indices = np.concatenate([np.zeros(ref_start_pad), ref.indices, np.zeros(ref_end_pad)])
    # mut_indices = np.concatenate([np.zeros(var_start_pad),  var.indices, np.zeros(var_end_pad)])
    #
    # ref_indices = ref_indices[context:-context]
    # mut_indices = mut_indices[context:-context]
    #
    # ref_seq = 'N'*ref_start_pad + ref.seq + 'N'*ref_end_pad
    # var_seq = 'N'*var_start_pad + var.seq + 'N'*var_end_pad
    #
    # if engine == 'spliceai':
    #     from .spliceai_utils import sai_predict_probs, sai_models
    #     ref_seq_acceptor_probs, ref_seq_donor_probs = sai_predict_probs(ref_seq, models=sai_models)
    #     mut_seq_acceptor_probs, mut_seq_donor_probs = sai_predict_probs(var_seq, models=sai_models)
    #
    # elif engine == 'pangolin':
    #     from .pangolin_utils import pangolin_predict_probs, pang_models
    #     ref_seq_donor_probs, ref_seq_acceptor_probs = pangolin_predict_probs(ref_seq, models=pang_models, just_ss=just_ss)
    #     mut_seq_donor_probs, mut_seq_acceptor_probs = pangolin_predict_probs(var_seq, models=pang_models, just_ss=just_ss)
    #
    # else:
    #     raise ValueError(f"{engine} not implemented")
    #
    # visible_donors = np.intersect1d(transcript.donors, ref_indices)
    # visible_acceptors = np.intersect1d(transcript.acceptors, ref_indices)
    #
    # assert len(ref_indices) == len(ref_seq_acceptor_probs), f'Reference pos ({len(ref_indices)}) not the same as probs ({len(ref_seq_acceptor_probs)})'
    # assert len(mut_indices) == len(mut_seq_acceptor_probs), f'Mut pos ({len(mut_indices)}) not the same as probs ({len(mut_seq_acceptor_probs)})'
    #
    # iap, dap = find_ss_changes({p: v for p, v in list(zip(ref_indices, ref_seq_acceptor_probs))},
    #                            {p: v for p, v in list(zip(mut_indices, mut_seq_acceptor_probs))},
    #                            visible_acceptors,
    #                            threshold=threshold)
    #
    # assert len(ref_indices) == len(ref_seq_donor_probs), 'Reference pos not the same'
    # assert len(mut_indices) == len(mut_seq_donor_probs), 'Mut pos not the same'
    #
    # idp, ddp = find_ss_changes({p: v for p, v in list(zip(ref_indices, ref_seq_donor_probs))},
    #                            {p: v for p, v in list(zip(mut_indices, mut_seq_donor_probs))},
    #                            visible_donors,
    #                            threshold=threshold)
    #
    # ref_acceptors = {a: b for a, b in list(zip(ref_indices, ref_seq_acceptor_probs))}
    # ref_donors = {a: b for a, b in list(zip(ref_indices, ref_seq_donor_probs))}
    #
    # lost_acceptors = {int(p): {'absolute': np.float64(0), 'delta': round(float(-ref_acceptors[p]), 3)} for p in
    #                   visible_acceptors if p not in mut_indices and p not in dap}
    # lost_donors = {int(p): {'absolute': np.float64(0), 'delta': round(float(-ref_donors[p]), 3)} for p in visible_donors
    #                if p not in mut_indices and p not in ddp}
    # dap.update(lost_acceptors)
    # ddp.update(lost_donors)
    #
    # missplicing = {'missed_acceptors': dap, 'missed_donors': ddp, 'discovered_acceptors': iap, 'discovered_donors': idp}
    # missplicing = {outk: {float(k): v for k, v in outv.items()} for outk, outv in missplicing.items()}
    # temp =  {outk: {int(k) if k.is_integer() else k: v for k, v in outv.items()} for outk, outv in missplicing.items()}
    return temp


def find_transcript_missplicing_seqs(ref_seq, var_seq, donors, acceptors, threshold=0.5, engine='spliceai'):
    if ref_seq.seq == var_seq.seq:
        return {'missed_acceptors': {}, 'missed_donors': {}, 'discovered_acceptors': {}, 'discovered_donors': {}}

    ref_seq_acceptor_probs, ref_seq_donor_probs = run_splicing_engine(ref_seq.seq, engine)
    mut_seq_acceptor_probs, mut_seq_donor_probs = run_splicing_engine(var_seq.seq, engine)
    ref_indices = ref_seq.indices[5000:-5000]
    mut_indices = var_seq.indices[5000:-5000]
    visible_donors = np.intersect1d(donors, ref_indices)
    visible_acceptors = np.intersect1d(acceptors, ref_indices)

    assert len(ref_indices) == len(
        ref_seq_acceptor_probs), f'Reference pos ({len(ref_indices)}) not the same as probs ({len(ref_seq_acceptor_probs)})'
    assert len(mut_indices) == len(
        mut_seq_acceptor_probs), f'Mut pos ({len(mut_indices)}) not the same as probs ({len(mut_seq_acceptor_probs)})'

    iap, dap = find_ss_changes({p: v for p, v in list(zip(ref_indices, ref_seq_acceptor_probs))},
                               {p: v for p, v in list(zip(mut_indices, mut_seq_acceptor_probs))},
                               visible_acceptors,
                               threshold=0.1)

    assert len(ref_indices) == len(ref_seq_donor_probs), 'Reference pos not the same'
    assert len(mut_indices) == len(mut_seq_donor_probs), 'Mut pos not the same'

    idp, ddp = find_ss_changes({p: v for p, v in list(zip(ref_indices, ref_seq_donor_probs))},
                               {p: v for p, v in list(zip(mut_indices, mut_seq_donor_probs))},
                               visible_donors,
                               threshold=0.1)

    ref_acceptors = {a: b for a, b in list(zip(ref_indices, ref_seq_acceptor_probs))}
    ref_donors = {a: b for a, b in list(zip(ref_indices, ref_seq_donor_probs))}

    lost_acceptors = {int(p): {'absolute': np.float64(0), 'delta': round(float(-ref_acceptors[p]), 3)} for p in
                      visible_acceptors if p not in mut_indices and p not in dap}
    lost_donors = {int(p): {'absolute': np.float64(0), 'delta': round(float(-ref_donors[p]), 3)} for p in
                   visible_donors
                   if p not in mut_indices and p not in ddp}
    dap.update(lost_acceptors)
    ddp.update(lost_donors)

    missplicing = {'missed_acceptors': dap, 'missed_donors': ddp, 'discovered_acceptors': iap,
                   'discovered_donors': idp}
    missplicing = {outk: {float(k): v for k, v in outv.items()} for outk, outv in missplicing.items()}
    temp = {outk: {int(k) if k.is_integer() else k: v for k, v in outv.items()} for outk, outv in
            missplicing.items()}
    return Missplicing(temp, threshold=threshold)


class Missplicing:
    def __init__(self, splicing_dict, threshold=0.5):
        """
        Initialize a Missplicing object.

        Args:
            splicing_dict (dict): Dictionary containing splicing events and their details.
                                  Example:
                                  {
                                    "missed_acceptors": {100: {"absolute": 0.0, "delta": -0.3}, ...},
                                    "missed_donors": { ... },
                                    "discovered_acceptors": { ... },
                                    "discovered_donors": { ... }
                                  }
            threshold (float): The threshold above which a delta is considered significant.
        """
        self.missplicing = splicing_dict
        self.threshold = threshold

    def __str__(self):
        """String representation displays the filtered splicing events passing the threshold."""
        return str(self.significant_events)

    def __bool__(self):
        """
        Boolean evaluation: True if any event surpasses the threshold, False otherwise.
        """
        return self.first_significant_event() is not None

    def __iter__(self):
        """
        Iterate over all delta values from all events. The first yielded value is 0 (for compatibility),
        followed by all deltas in self.missplicing.
        """
        yield 0
        for details in self.missplicing.values():
            for d in details.values():
                yield d['delta']

    @property
    def aberrant_splicing(self):
        """
        Returns a filtered version of missplicing events that meet or exceed the current threshold.
        """
        return self.filter_by_threshold(self.threshold)

    def filter_by_threshold(self, threshold=None):
        """
        Filter self.missplicing to only include events where abs(delta) >= threshold.

        Args:
            threshold (float, optional): The threshold to apply. Defaults to self.threshold.

        Returns:
            dict: A new dictionary with filtered events.
        """
        if threshold is None:
            threshold = self.threshold

        return {
            event: {
                pos: detail for pos, detail in details.items()
                if abs(detail['delta']) >= threshold
            }
            for event, details in self.missplicing.items()
        }

    def first_significant_event(self, splicing_dict=None, threshold=None):
        """
        Check if there is any event surpassing a given threshold and return the dictionary if found.

        Args:
            splicing_dict (dict, optional): Dictionary to check. Defaults to self.missplicing.
            threshold (float, optional): Threshold to apply. Defaults to self.threshold.

        Returns:
            dict or None: Returns the dictionary if a delta surpasses the threshold, otherwise None.
        """
        if splicing_dict is None:
            splicing_dict = self.missplicing
        if threshold is None:
            threshold = self.threshold

        # Check if any event meets the threshold
        if any(abs(detail['delta']) >= threshold for details in splicing_dict.values() for detail in details.values()):
            return splicing_dict
        return None

    def max_delta(self):
        """
        Returns the maximum absolute delta found in all events.

        Returns:
            float: The maximum absolute delta, or 0 if no events.
        """
        deltas = [detail['delta'] for details in self.missplicing.values() for detail in details.values()]
        return max(deltas, key=abs, default=0.0)


# def find_transcript_splicing(transcript, engine='spliceai'):
#     ref_indices = transcript.indices
#     ref_seq = 'N' * 5000 + transcript.seq + 'N' * 5000
#     if engine == 'spliceai':
#         from .spliceai_utils import sai_predict_probs, sai_models
#         ref_seq_acceptor_probs, ref_seq_donor_probs = sai_predict_probs(ref_seq, sai_models)
#
#     elif engine == 'pangolin':
#         from .pangolin_utils import pangolin_predict_probs, pang_models
#         ref_seq_donor_probs, ref_seq_acceptor_probs = pangolin_predict_probs(ref_seq, models=pang_models)
#
#     else:
#         raise ValueError(f"{engine} not implemented")
#
#     assert len(ref_seq_donor_probs) == len(ref_indices), f'{len(ref_seq_donor_probs)}  vs. {len(ref_indices)}'
#     donor_probs = {i: p for i, p in list(zip(ref_indices, ref_seq_donor_probs))}
#     donor_probs = dict(sorted(donor_probs.items(), key=lambda item: item[1], reverse=True))
#
#     acceptor_probs = {i: p for i, p in list(zip(ref_indices, ref_seq_acceptor_probs))}
#     acceptor_probs = dict(sorted(acceptor_probs.items(), key=lambda item: item[1], reverse=True))
#     return donor_probs, acceptor_probs


def benchmark_splicing(gene, organism='hg38', engine='spliceai'):
    gene = Gene(gene, organism=organism)
    transcript = gene.transcript()
    if len(transcript.introns) == 0:
        return None, None

    transcript.generate_pre_mrna()
    predicted_donor_sites, predicted_acceptor_sites = find_transcript_splicing(transcript.pre_mrna, engine=engine)
    num_introns = len(transcript.introns)
    predicted_donors = list(predicted_donor_sites.keys())[:num_introns]
    predicted_acceptors = list(predicted_acceptor_sites.keys())[:num_introns]
    correct_donor_preds = [v for v in predicted_donors if v in transcript.donors]
    correct_acceptor_preds = [v for v in predicted_acceptors if v in transcript.acceptors]
    return len(correct_donor_preds) / num_introns, len(correct_acceptor_preds) / num_introns, len(transcript.introns)


import sqlite3
import json
import os

# Global connection and cursor (adjust to your architecture)
# Ideally, initialize this once in your application startup code.
DB_PATH = os.path.join(config['hg38']['splicing_db'], 'mutation_data.db')
conn = sqlite3.connect(DB_PATH, isolation_level=None)  # autocommit mode
cursor = conn.cursor()

# Create table once at startup, not in the function
cursor.execute('''
CREATE TABLE IF NOT EXISTS mutations (
    tool TEXT,
    gene TEXT,
    mutation_id TEXT,
    transcript_id TEXT,
    data TEXT,
    PRIMARY KEY (tool, gene, mutation_id, transcript_id)
)''')

def get_or_compute_splicing(tool, gene, mutation_id, transcript_id, force_recompute=False):
    """
    Retrieve computed splicing data for a given mutation from a database,
    or compute and store it if not found or if force_recompute is True.

    Args:
        tool (str): Name of the tool used for computation.
        gene (str): Gene name or identifier.
        mutation_id (str): A unique identifier for the mutation.
        transcript_id (str): ID for the transcript.
        force_recompute (bool): If True, ignore cached value and recompute.

    Returns:
        dict: The computed splicing data.
    """

    # Lookup in the database
    cursor.execute('SELECT data FROM mutations WHERE tool=? AND gene=? AND mutation_id=? AND transcript_id=?',
                   (tool, gene, mutation_id, transcript_id))
    row = cursor.fetchone()

    # If found and no force recompute, return cached data
    if row and not force_recompute:
        return json.loads(row[0])

    # Otherwise, compute the data
    computed_data = find_transcript_missplicing(mutation_id, transcript_id=transcript_id, engine=tool)  # Replace with your actual function

    # Store computed data in DB
    data_json = json.dumps(computed_data)
    cursor.execute('REPLACE INTO mutations (tool, gene, mutation_id, transcript_id, data) VALUES (?, ?, ?, ?, ?)',
                   (tool, gene, mutation_id, transcript_id, data_json))

    return computed_data