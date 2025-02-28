<?php

// Atur header
header("Content-Type: application/json");

// Data array pesanan barang
$pesanan = array(
    array('id' => 1, 'name' => 'Sepatu Nike Nitro', 'harga' => 900000),
    array('id' => 2, 'name' => 'Celana Eiger Retro', 'harga' => 560000),
    array('id' => 3, 'name' => 'Kaos Google Pro', 'harga' => 280000)
);

// Menggunakan Method GET
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    // Return the list of users as JSON
    echo json_encode($pesanan);
} else {
    // Jika terjadi error, mengirimkan pesan error
    http_response_code(405);
    $error = array('error' => 'Barang kamu dibawa lari kurir');
    echo json_encode($error);
}
