<?php
$input_data = json_decode(file_get_contents('php://input'), true);
if (array_key_exists('app_name', $input_data)) {
    $app_name = $input_data['app_name'];
    $scoop_directory_db = __DIR__ . '/scoop_directory.db';
    $db = new SQLite3($scoop_directory_db);
    $stm = $db->prepare('SELECT * FROM main.app WHERE name LIKE ? ORDER BY version DESC');
    $stm->bindValue(1, '%' . $app_name . '%', SQLITE3_TEXT);
    $res = $stm->execute();
    $app_names = [];
    $app_versions = [];
    $app_bucket_repos = [];
    $app_names[] = 'app_name';
    $app_versions[] = 'app_version';
    $app_bucket_repos[] = 'bucket_repo';
    while ($scoop_apps = $res->fetchArray(SQLITE3_ASSOC)) {
        $app_names[] = $scoop_apps['name'];
        $app_versions[] = $scoop_apps['version'];
        $app_bucket_repos[] = $scoop_apps['bucket_repo'];
    }
    $app_names = format_arr($app_names);
    $app_versions = format_arr($app_versions);
    $app_bucket_repos = format_arr($app_bucket_repos);
    $query_result = '';
    $i = 0;
    while ($i < count($app_names)) {
        if ($i < count($app_names) - 1) {
            $query_result.= "{$app_names[$i]}\t{$app_versions[$i]}\t{$app_bucket_repos[$i]}\n";
        } else {
            $query_result.= "{$app_names[$i]}\t{$app_versions[$i]}\t{$app_bucket_repos[$i]}";
        }
        $i+= 1;
    }
    echo $query_result;
} else {
    echo '';
}
function max_length_of_line($arr)
{
    $max_len = 0;
    foreach ($arr as $key => $line) {
        if (strlen($line) > $max_len) {
            $max_len = strlen($line);
        }
    }
    return $max_len;
}
function format_arr($arr)
{
    $max_len = max_length_of_line($arr);
    for ($i = 0; $i < count($arr); $i++) {
        $line = $arr[$i];
        if (strlen($line) !== $max_len) {
            $multiplier = $max_len - strlen($line);
            $spaces = str_repeat(' ', $multiplier);
            $arr[$i] = "{$line}{$spaces}";
        }
    }
    return $arr;
}
