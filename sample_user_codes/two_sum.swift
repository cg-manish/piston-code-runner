class Solution {
    func twoSum(_ nums: [Int], _ target: Int) -> [Int] {
        var map = [Int: Int]()
        for (i, num) in nums.enumerated() {
            let complement = target - num
            if let index = map[complement] {
                return [index, i]
            }
            map[num] = i
        }
        return []
    }
}

