# Plan:
# Store all the url's into an array. Call dig on all
# the url's in the array 10 times, storing the times it took
# to query in each trial into an array. Combine all 10 arrays that
# were produced into a bigger array and print the values into
# a csv file

$urls = "google.com", "youtube.com", "Baidu.com", "yahoo.com", "amazon.com", "wikipedia.org", "zoom.us", "facebook.com", "reddit.com", "netflix.com"

# experiment2 (replace with dig `@8.8.8.8 for experiment3)
$allTimes = @()
for($j=0; $j -lt 10; $j++) {
    $url = $urls[$j]
    $times = @()
    for($i = 0; $i -lt 10; $i++) {
        $start = Get-Date
        dig `@8.8.8.8 $url
        $end = Get-Date 
        $diff = $end-$start
        $diff = $diff.TotalSeconds
        # $allTimes += diff
        $times += $diff
    }
    # $allTimes.Count
    $allTimes += $times
}
# $allTimes

# Print contents of allTimes to a CSV file
# Print File Headers
for($i=0; $i -lt 10; $i++) {
    if($i -eq 9) {
        $urls[$i] | Out-File -FilePath ".\experiment3.csv" -Append -Encoding utf8
    }
    else {
        $urls[$i]+", " | Out-File -FilePath ".\experiment3.csv" -Append -NoNewline -Encoding utf8
    }
}
# Print query times
for($i=0; $i -lt 10; $i++) {
    for($j=0; $j -lt 100; $j+=10) {
        if($j+10 -ge 100) {
            [string]$allTimes[$i+$j] | Out-File -FilePath ".\experiment3.csv" -Append -Encoding utf8
        }
        else {
            [string]$allTimes[$i+$j]+", " | Out-File -FilePath ".\experiment3.csv" -Append -NoNewline -Encoding utf8
        }
    }
}