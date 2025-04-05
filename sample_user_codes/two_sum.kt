class Solution {
    fun twoSum(nums: IntArray, target: Int): IntArray {
        val map = mutableMapOf<Int, Int>()
        nums.forEachIndexed { i, num ->
            val complement = target - num
            if (map.contains(complement)) {
                return intArrayOf(map[complement]!!, i)
            }
            map[num] = i
        }
        return intArrayOf()
    }
}

