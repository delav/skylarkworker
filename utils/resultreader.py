

def suite_result_handler(result_str):
    state_count = {}
    state_strs = result_str.split(',')
    for item in state_strs:
        cs = item.split()
        state_count[cs[1]] = cs[0]
    return state_count
