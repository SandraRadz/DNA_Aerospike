local function one(rec)
    return 1
end

local function add(a, b)
    return a + b
end

function count(stream)
    return stream : map(one) : reduce(add);
end

-- ############################################################## --

function diff_num(rec)
    return #rec["difference"]
end

-- 1453 --
function total_diff_num(stream)
    return stream : map(diff_num) : reduce(add);
end

-- ############################################################## --
function count_position(rec)
    fasta = "TTCTTTCATGGGGAAGCAGATTTGGGTACCACCCAAGTATTGACTCACCCATCAACAACCGCTATGTATTTCGTACATTACTGCCAGCCACCATGAATATTGTACAGTACCATAAATACTTGACCACCTGTAGTACATAAAAACCCAATCCACATCAAAACCCTCCCCCCATGCTTACAAGCAAGTACAGCAATCAACCTTCAACTGTCACACATCAACTGCAACTCCAAAGCCACCCCTCACCCACTAGGATATCAACAAACCTACCCACCCTTAACAGTACATAGCACATAAAGCCATTTACCGTACATAGCACATTACAGTCAAATCCCTTCTCGTCCCCATGGATGACCCCCCTCAGATAGGGGTCCCTTGAC"
    result = map()
    len = #fasta
    for i=1,len do
        if rec["difference"][i] ~= nil then
            symbol = rec["difference"][i]
        else
            symbol = string.sub(fasta, i, i)
        end
        sub_res = map()
        if symbol == "A" then
            sub_res[1] = 1
            sub_res[2] = 0
            sub_res[3] = 0
            sub_res[4] = 0
            sub_res[5] = 0
        elseif symbol == "C" then
            sub_res[1] = 0
            sub_res[2] = 1
            sub_res[3] = 0
            sub_res[4] = 0
            sub_res[5] = 0
        elseif symbol == "G" then
            sub_res[1] = 0
            sub_res[2] = 0
            sub_res[3] = 1
            sub_res[4] = 0
            sub_res[5] = 0
        elseif symbol == "T" then
            sub_res[1] = 0
            sub_res[2] = 0
            sub_res[3] = 0
            sub_res[4] = 1
            sub_res[5] = 0
        else
            sub_res[1] = 0
            sub_res[2] = 0
            sub_res[3] = 0
            sub_res[4] = 0
            sub_res[5] = 1
        end
        result[i] = sub_res
    end
    return result
end

function collect_positions(rec1, rec2)
    len = #rec1
    for i=1,len do
        for j=1,5 do
            rec1[i][j] = rec1[i][j] + rec2[i][j]
        end
    end
    return rec1
end

local function find_max(dict)
    max_num = dict[1]
    max_value = "A"
    values = {"A", "C", "G", "T", "?"}
    for i=1,#dict do
        if dict[i] > max_num then
            max_num = dict[i]
            max_value = values[i]
        end
    end
    return max_value
end

function show_result(rec)
    res = ""
    for i=1,#rec do
        max = find_max(rec[i])
        res = res..max
    end
    return res
end

-- TTCTTTCATGGGGAAGCAGATTTGGGTACCACCCAAGTATTGACTCACCCATCAACAACCGCTATGTATTTCGTACATTACTGCCAGCCACCATGAATATTGTAGAGTACCATAAATACTTGACCACCTGTAGTACATAAAAACCCAATCCACATCAAAACCCTTCCCCCATGCTTACAAGCAAGTACAGCAATCAACCTTCAACAGTCACACATCAACTGCAACTCCAAAGCCACCCCTCACCCACTAGGATCTCAACAAACCTACCCACCCTTAACAGTACATATCACATAAAGCCATTTACCGTACATAGCACATTACAGTCAAATCCCTTCTCGTCCCCATGGATGACCCCCCTCAGATAGGGGTCCCTTGAC
function wild_type(stream)
    return stream : map(count_position) : reduce(collect_positions) : map(show_result)
end