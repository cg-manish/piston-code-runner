def two_sum(nums, target)
    map = {}
    nums.each_with_index do |num, i|
        complement = target - num
        return [map[complement], i] if map.key?(complement)
        map[num] = i
    end
end

