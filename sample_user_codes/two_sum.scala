object Solution {
    def twoSum(nums: Array[Int], target: Int): Array[Int] = {
        val map = scala.collection.mutable.HashMap[Int, Int]()
        for (i <- nums.indices) {
            val complement = target - nums(i)
            if (map.contains(complement)) return Array(map(complement), i)
            map(nums(i)) = i
        }
        Array()
    }
}

