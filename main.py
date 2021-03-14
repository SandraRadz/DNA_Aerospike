import csv
import sys

import aerospike

from query import dif_to_base_sequence, total_diff_num, wild_type
from settings import config, NAMESPACE, BASE_SEQUENCE, SET


def read_csv(filename):
    with open(filename) as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        for row in reader:
            yield row


def insert_sequence(client, url, region, fasta, name=None):
    key = (NAMESPACE, SET, fasta)
    (k, meta) = client.exists(key)
    if meta:
        owner = {"region": region, "url": url}
        client.list_append(key, "owner", owner)
    else:
        bins = {
            "owner": [{"region": region, "url": url}],
            "length": len(fasta),
            "difference": calc_diff(fasta, BASE_SEQUENCE),
            "name": name
        }
        client.put(key, bins)


def print_result(record_tuple):
    key, metadata, record = record_tuple
    print(key, metadata, record)


def calc_diff(fasta, base_fasta):
    res = {}
    if len(fasta) == len(base_fasta):
        for i in range(len(fasta)):
            if fasta[i] != base_fasta[i]:
                res[i] = fasta[i]
    return res


def fullfill_db_with_data(client):
    rows = read_csv("result.csv")
    next(rows, None)

    done = 0
    total_dif_num = 0

    # add Eva
    insert_sequence(client, "EVA", "", BASE_SEQUENCE, "EVA")

    for row in rows:
        url = row[0]
        region = row[1]
        fasta = row[2]
        insert_sequence(client, url, region, fasta)
        done += 1
    # scan = client.scan(NAMESPACE, SET)
    # scan.foreach(print_result)


def run_query(client):

    total_diff_num(client)
    wild_type(client)


if __name__ == '__main__':
    try:
        aerospike_client = aerospike.client(config)
        aerospike_client.connect()
    except Exception as e:
        print("error: {0}".format(e), file=sys.stderr)
        sys.exit(1)

    # fullfill_db_with_data(aerospike_client)

    aerospike_client.udf_put('custom_functions.lua')

    run_query(aerospike_client)

    aerospike_client.close()

