<?php
class MeuBanco
{
    private $host = "127.0.0.1";
    private $usuario = "root";
    private $senha = "";
    private $banco = "feira";
    private $porta = "3307";
    private $con = null;

    private function conectar()
    {
        $this->con = new mysqli($this->host, $this->usuario, $this->senha, $this->banco, $this->porta);
        if ($this->con->connect_error) {
            $resposta['erro'] = $this->con->connect_error;
            echo json_encode($resposta['erro']);
            die();
        }
    }

    public function getConexao()
    {
        if ($this->con == null) {
            $this->conectar();
        }
        return $this->con;
    }
}

$banco = new MeuBanco();
$stmt = $banco->getConexao()->prepare("SELECT * FROM polichinelo ORDER BY contpol DESC LIMIT 5");
$stmt->execute();
$resultados = $stmt->get_result();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ranking Polichinelos</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }

        h1 {
            text-align: center;
            background-color: #333;
            color: #fff;
            padding: 10px 0;
            margin: 0;
        }

        table {
            width: 80%;
            margin: 20px auto;
            border-collapse: collapse;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        th, td {
            text-align: left;
            padding: 12px;
        }

        th {
            background-color: #333;
            color: #fff;
        }

        tr:nth-child(even) {
            background-color: #f2f2f2;
        }

        tr:hover {
            background-color: #ddd;
        }

        .rank {
            font-weight: bold;
        }

        .gold {
            color: #ffd700;
        }

        .silver {
            color: #c0c0c0;
        }

        .bronze {
            color: #cd7f32;
        }
    </style>
</head>
<body>
    <h1>Ranking Polichinelos</h1>
    <table>
        <tr>
            <th>Posição</th>
            <th>Nome</th>
            <th>Pontuação</th>
            <th>Instagram</th>
        </tr>
        <?php
        $posicao = 1;
        while ($row = $resultados->fetch_assoc()) {
            $id = $row['idusuario'];
            $pol = $row['contpol'];

            $stmt2 = $banco->getConexao()->prepare("SELECT nome FROM Usuarios WHERE id = ?");
            $stmt2->bind_param("i", $id);
            $stmt2->execute();
            $result2 = $stmt2->get_result();
            $row2 = $result2->fetch_assoc();
            $nome = $row2['nome'];

            $stmt3 = $banco->getConexao()->prepare("SELECT insta FROM Usuarios WHERE id = ?");
            $stmt3->bind_param("i", $id);
            $stmt3->execute();
            $result3 = $stmt3->get_result();
            $row3 = $result3->fetch_assoc();
            $insta = $row3['insta'];

            ?>
            <tr>
                <td class="rank <?php echo ($posicao == 1) ? 'gold' : (($posicao == 2) ? 'silver' : (($posicao == 3) ? 'bronze' : '')); ?>"><?php echo $posicao . "º"; ?></td>
                <td><?php echo $nome; ?></td>
                <td><?php echo $pol; ?></td>
                <td><a href="<?php echo "https://www.instagram.com/$insta/"; ?>"><?php echo "@".$insta; ?></a></td>
            </tr>
            <?php
            $stmt2->close(); // Fechar a consulta preparada $stmt2
            $stmt3->close(); // Fechar a consulta preparada $stmt3
            $posicao++;
        }
        ?>
    </table>
</body>
</html>
