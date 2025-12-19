<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Resultado</title>
</head>
<body>

<h2>Resultado da Operação</h2>

<p>
<?php
echo htmlspecialchars($_GET['resposta'] ?? 'Nenhum resultado encontrado');
?>
</p>

<a href="index.php">Voltar</a>

</body>
</html>
