<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Cliente PHP - Calculadora</title>
</head>
<body>

<h2>Calculadora via API Spring Boot</h2>

<form action="calcular.php" method="GET">
    <input type="number" name="num1" placeholder="Número 1" required>
    <input type="number" name="num2" placeholder="Número 2" required>

    <select name="operacao">
        <option value="somar">Somar</option>
        <option value="subtrair">Subtrair</option>
        <option value="multiplicar">Multiplicar</option>
        <option value="dividir">Dividir</option>
    </select>

    <button type="submit">Calcular</button>
</form>

</body>
</html>
