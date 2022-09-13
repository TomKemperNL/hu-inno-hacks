from os.path import exists
import json


def cache_list(filename, clz, func):
    def wrapper(*args, **kwargs):
        if exists(filename):
            with open(filename) as f:
                raw = json.load(f)
                results = []
                for r in raw:
                    results.append(clz.from_dict(r))
                return results
        else:
            fresh_results = func(*args, **kwargs)
            with open(filename, 'w') as f:
                dict_results = list(map(lambda r: r.to_json(), fresh_results))
                json.dump(dict_results, f)

            return fresh_results

    return wrapper


def cache(filename, clz, func):
    def wrapper(*args, **kwargs):
        if exists(filename):
            with open(filename) as f:
                raw = json.load(f)
                return clz.from_dict(raw)
        else:
            fresh_result = func(*args, **kwargs)
            with open(filename, 'w') as f:
                dict_result = fresh_result.to_json()
                json.dump(dict_result, f)

            return fresh_result

    return wrapper
