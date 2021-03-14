# from aerospike import predicate

from settings import NAMESPACE, SET

# Currently, User-Defined Functions are written in Lua.


def simple_query(client):
    query = client.query(NAMESPACE, SET)
    query.select("url", "length")


def print_result(value):
    print(value)

# SELECT * FROM test.fasta WHERE PK="TTCTTTCATGGGGAAGCAGATTTGGGTACCACCCAAGTATTGACTCACCCATCAACAACCGCTATGTATTTCGTACATTACTGCCAGCCACCATGAATATTGTACGGTACCATAAATACTTGACCACCTGTAGTACATAAAAACCCAATCCACATCAAAACCCCCTCCCCATGCTTACAAGCAAGTACAGCAATCAACCCTCAACTATCACACATCAACTGCAACTCCAAAGCCACCCCTCACCCACTAGGATACCAACAAACCTACCCACCCTCAACAGTACATAGTACATAAAGCCATTTACCGTACATAGCACATTACAGTCAAATCCCTTCTCGTCCCCATGGATGACCCCCCTCAGATAGGGGTCCCTTGAC"


# EXECUTE custom_functions.diff_num() ON test.fasta WHERE PK="TTCTTTCATGGGGAAGCAGATTTGGGTACCACCCAAGTATTGACTCACCCATCAACAACCGCTATGTATTTCGTACATTACTGCCAGCCACCATGAATATTGTACGGTACCATAAATACTTGACCACCTGTAGTACATAAAAACCCAATCCACATCAAAACCCCCTCCCCATGCTTACAAGCAAGTACAGCAATCAACCCTCAACTATCACACATCAACTGCAACTCCAAAGCCACCCCTCACCCACTAGGATACCAACAAACCTACCCACCCTCAACAGTACATAGTACATAAAGCCATTTACCGTACATAGCACATTACAGTCAAATCCCTTCTCGTCCCCATGGATGACCCCCCTCAGATAGGGGTCCCTTGAC"
def dif_to_base_sequence(client, fasta):
    key1 = (NAMESPACE, SET, fasta)
    # query = client.query(NAMESPACE, SET)
    # query.where(predicate.equals("PK", fasta))
    # query.apply("custom_functions", "diff_num", [])


# total num of difference
# AGGREGATE custom_functions.total_diff_num() ON test.fasta
def total_diff_num(client):
    query = client.query(NAMESPACE, SET)
    query.apply("custom_functions", "total_diff_num", [])
    query.foreach(print_result)

# AGGREGATE custom_functions.wild_type() ON test.fasta
def wild_type(client):
    query = client.query(NAMESPACE, SET)
    query.apply("custom_functions", "wild_type", [])
    query.foreach(print_result)
