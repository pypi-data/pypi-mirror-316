def calculate_level_averages(numbers, key=None, levels=5):
    """
    Calculates level averages and fits a linear interpolation function
    to the input numbers. It returns ranges and counts based on the predicted
    function.

    Args:
        numbers (list): The array of numbers to process or objects containing numbers.
        key (str, optional): The key to access the number in each object if 'numbers' is a list of objects. Defaults to None.
        levels (int, optional): The number of levels (must be odd and > 2). Defaults to 5.

    Returns:
        dict: Dictionary containing bins (level objects with range, count, avg, min, max) and a get function to retrieve statistics for a given number.
    """

    if key:
        src_numbers = [item[key] for item in numbers]
    else:
        src_numbers = numbers[:]  # Create a copy to avoid modifying the original list

    src_numbers.sort()

    if not isinstance(src_numbers, list) or len(src_numbers) == 0:
        raise ValueError("Input must be a non-empty list of numbers.")

    if levels < 3 or levels % 2 == 0:
        raise ValueError("Levels must be odd and greater than 2.")

    middle_level_index = levels // 2
    level_array = [{} for _ in range(levels)]

    def calculate_avg(arr):
        return sum(arr) / len(arr) if len(arr) > 0 else 0

    middle_avg = calculate_avg(src_numbers)
    middle_count = len(src_numbers)

    level_array[middle_level_index] = {
        "actual_avg": middle_avg,
        "actual_count": middle_count
    }

    previous_up_level = src_numbers
    previous_down_level = src_numbers

    for i in range(middle_level_index + 1, levels):
        level = [num for num in previous_up_level if num > level_array[i - 1]["actual_avg"]]
        previous_up_level = level
        level_avg = calculate_avg(level)
        level_count = len(level)

        level_array[i] = {
            "actual_avg": level_avg,
            "actual_count": level_count
        }

    for i in range(middle_level_index - 1, -1, -1):
        level = [num for num in previous_down_level if num < level_array[i + 1]["actual_avg"]]
        previous_down_level = level
        level_avg = calculate_avg(level)
        level_count = len(level)

        level_array[i] = {
            "actual_avg": level_avg,
            "actual_count": level_count
        }

    first_non_zero_index = next((i for i, level in enumerate(level_array) if level["actual_count"] > 0), 0)
    last_non_zero_index = len(level_array) - 1 - next((i for i, level in enumerate(reversed(level_array)) if level["actual_count"] > 0), 0)

    points = []
    for idx, level in enumerate(level_array):
        if first_non_zero_index <= idx <= last_non_zero_index:
            points.append((idx, level["actual_avg"]))

    scale_factor = (last_non_zero_index - first_non_zero_index) / (levels - 1)

    def input_scale(value):
      return first_non_zero_index + value * scale_factor

    def linear_predict(points, idx):
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            if x1 <= idx <= x2:
                slope = (y2 - y1) / (x2 - x1)
                intercept = y1 - slope * x1
                return slope * idx + intercept
        raise ValueError("Index is outside the range of points.")
    
    def stats(data, dir="range", value=None, max_val=None):
      count = 0
      sum_val = 0
      bucket_min = float('inf')
      bucket_max = float('-inf')

      if dir == 'down':
          for num in data:
              if num < value:
                  count += 1
                  sum_val += num
                  bucket_max = max(bucket_max, num)
                  bucket_min = min(bucket_min, num)
      elif dir == 'up':
          for num in data:
              if num >= value:
                  count += 1
                  sum_val += num
                  bucket_max = max(bucket_max, num)
                  bucket_min = min(bucket_min, num)
      elif dir == 'range':
          for num in data:
              if value <= num < max_val:
                  count += 1
                  sum_val += num
                  bucket_max = max(bucket_max, num)
                  bucket_min = min(bucket_min, num)

      return {
          "count": count,
          "avg": sum_val / count if count > 0 else 0,
          "min": bucket_min,
          "max": bucket_max
      }

    predicts = [linear_predict(points, input_scale(idx)) for idx in range(levels)]
    result = []

    for i in range(levels):
        if i == 0:
            result.append({
                "range": [float('-inf'), predicts[i]],
                **stats(src_numbers, 'down', predicts[i])
            })
            result.append({
                "range": [predicts[i], predicts[i + 1]],
                **stats(src_numbers, 'range', predicts[i], predicts[i + 1])
            })
        elif i == levels - 1:
            result.append({
                "range": [predicts[i - 1], predicts[i]],
                **stats(src_numbers, 'range', predicts[i - 1], predicts[i])
            })
            result.append({
                "range": [predicts[i], float('inf')],
                **stats(src_numbers, 'up', predicts[i])
            })
        elif i == middle_level_index:
            result.append({
                "range": [predicts[i - 1], predicts[i + 1]],
                **stats(src_numbers, 'range', predicts[i - 1], predicts[i+1])
            })

        elif i != middle_level_index -1 and i != middle_level_index + 1:
          if i > middle_level_index:
            result.append({
              "range": [predicts[i-1], predicts[i]],
              **stats(src_numbers, 'range', predicts[i-1], predicts[i])
            })
          else:
            result.append({
              "range": [predicts[i], predicts[i+1]],
              **stats(src_numbers, 'range', predicts[i], predicts[i+1])
            })

    sum_counts = sum(level["count"] for level in result)
    if sum_counts != len(src_numbers):
        raise ValueError("Sum of counts does not match the length of the numbers array.")
    
    def get_position(value, bucket, fraction_digits=2):
      if bucket["count"] == 1:
        return 0.5
            
      min_val = bucket["min"]
      max_val = bucket["max"]

      if(min_val == max_val):
        return 0.5
      
      raw_position = (value - min_val) / (max_val - min_val)
      return round(raw_position, fraction_digits)
    
    def get_stats(number):
      level = None
      for i in range(len(result)):
        if result[i]["range"][0] == float('-inf') and number < result[i]["range"][1]:
            level = i
        elif result[i]["range"][1] == float('inf') and number >= result[i]["range"][0]:
            level = i
        elif result[i]["range"][0] <= number < result[i]["range"][1]:
          level = i
      
      if level is None:
        return None
      
      return {
        "bin": result[level],
        "level": level,
        "position": get_position(number, result[level])
      }
    
    return {
      "bins": result,
      "get": get_stats
    }

def default(**kwargs):
    return calculate_level_averages(**kwargs);

if __name__ == "__main__":
    import random

    # Generate a large list of numbers for testing
    numbers = [random.randint(1, 1000) for _ in range(1000)]
    levels = 5

    result = default(numbers=numbers, levels=levels)
    
    # Print the ranges
    print("Bins and Counts:")
    for idx, level in enumerate(result["bins"]):
        print(f"Level {idx}: Range {level['range']}, Count {level['count']}")

    # Test the `get` function for a specific number
    test_number = random.choice(numbers)
    level_of_test_number = result["get"](test_number)
    print(f"\nThe number {test_number} belongs to level {level_of_test_number}.")