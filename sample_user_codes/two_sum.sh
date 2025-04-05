# Bash isn't suited for algorithmic problems, but here’s a basic idea:
nums=(2 7 11 15)
target=9

for ((i=0; i<${#nums[@]}; i++)); do
  for ((j=i+1; j<${#nums[@]}; j++)); do
    if [ $((${nums[i]} + ${nums[j]})) -eq $target ]; then
      echo "$i $j"
      exit 0
    fi
  done
done
