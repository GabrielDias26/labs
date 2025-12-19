<?php
$num1 = $_GET['num1'] ?? 0;
$num2 = $_GET['num2'] ?? 0;
$operacao = $_GET['operacao'] ?? 'somar';

// garante float
$num1 = floatval($num1);
$num2 = floatval($num2);

$url = "http://localhost:8080/$operacao/$num1/$num2";

// inicia cURL
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

// executa
$resposta = curl_exec($ch);

// erro?
if ($resposta === false) {
    die("Erro ao chamar API: " . curl_error($ch));
}

curl_close($ch);

// redireciona
header("Location: resultado.php?resposta=" . urlencode($resposta));
exit;
