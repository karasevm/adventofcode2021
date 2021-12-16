import sys
from operator import mul
from functools import reduce

def parse_packet(packet: str) -> tuple[int, int, int]:

    version = int(packet[0:3], 2)
    p_type = int(packet[3:6], 2)
    final_parsed_index = 0
    version_sum = version
    result = 0
    children = []

    if p_type == 4:
        bit_string = ""
        for index in range(6,len(packet), 5):
            bit_string += packet[index+1:index+5]
            if packet[index] == "0":
                final_parsed_index = index+5
                break
        result += int(bit_string, 2)
    else:
        if packet[6] == "0":
            sub_packet_length = int(packet[7:22], 2)
            final_parsed_index = 22
            while final_parsed_index != 22 + sub_packet_length:
                child_version, child_offset, child_result = parse_packet(packet[final_parsed_index:22+sub_packet_length])
                children.append(child_result)
                final_parsed_index += child_offset
                version_sum += child_version
        else:
            sub_packet_count = int(packet[7:18], 2)
            last_offset = 18
            for i in range(sub_packet_count):
                child_version, child_offset, child_result = parse_packet(packet[last_offset:])
                children.append(child_result)
                last_offset += child_offset
                version_sum += child_version
            final_parsed_index = last_offset
    
    children_ints = [int(x) for x in children]
    match p_type:
        case 0:
            result = sum(children_ints)
        case 1:
            result = reduce(mul, children_ints)
        case 2:
            result = min(children_ints)
        case 3:
            result = max(children_ints)
        case 5:
            result = 1 if children_ints[0] > children_ints[1] else 0
        case 6:
            result = 1 if children_ints[0] < children_ints[1] else 0
        case 7:
            result = 1 if children_ints[1] == children_ints[0] else 0
    return version_sum, final_parsed_index, result

def part1(input_list: list[str]) -> int:
    binary_string = ""
    for char in input_list[0]:
        binary_string += ( bin(int('1' + char, 16))[3:] )
    result,_ ,_ =parse_packet(binary_string)
    return result


def part2(input_list: list[str]) -> int:
    binary_string = ""
    for char in input_list[0]:
        binary_string += ( bin(int('1' + char, 16))[3:] )
    _ ,_ ,result = parse_packet(binary_string)
    return result


if __name__ == "__main__":
    try:
        f = open(sys.argv[1], "r")
    except IOError:
        print("Error opening the file, try again")
        sys.exit(1)
    with f:
        lines = f.readlines()
        lines = [line.rstrip() for line in lines]
        f.close()
        print(
            f"Part 1 answer: {part1(lines)} Part 2 answer: {part2(lines)}")
