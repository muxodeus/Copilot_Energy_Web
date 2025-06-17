const express = require("express");
const { Pool } = require("pg");
require("dotenv").config();

const pool = new Pool({
    connectionString: process.env.DATABASE_URL || "postgresql://mediciones_w63r_user:mJmDFzYPGpwflXHBxmpx8LhxXHAhW2uP@dpg-d17grr95pdvs738che40-a.oregon-postgres.render.com/mediciones_w63r",
    ssl: {
        rejectUnauthorized: false  // This ensures an SSL connection is used without strict certificate validation
    }
});

const app = express();
app.use(express.json());

// ✅ Retrieve Data from PostgreSQL
app.get("/datos", async (req, res) => {
    try {
        const result = await pool.query(`
            SELECT 
                voltaje_a AS "voltaje_A", 
                voltaje_b AS "voltaje_B", 
                voltaje_c AS "voltaje_C",
                frecuencia, 
                demanda_potencia_activa_total, 
                timestamp
            FROM mediciones_w63r
            ORDER BY timestamp DESC
            LIMIT 50;
        `);
        res.json(result.rows);
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: "Error retrieving data" });
    }
});

// ✅ Insert Data into PostgreSQL
app.post("/recibir_datos", async (req, res) => {
    try {
        const { voltaje_A, voltaje_B, voltaje_C, frecuencia, demanda_potencia_activa_total, timestamp } = req.body;
        await pool.query(`
            INSERT INTO mediciones_w63r 
            (voltaje_a, voltaje_b, voltaje_c, frecuencia, demanda_potencia_activa_total, timestamp)
            VALUES ($1, $2, $3, $4, $5, $6)
        `, [voltaje_A, voltaje_B, voltaje_C, frecuencia, demanda_potencia_activa_total, timestamp]);
        res.json({ message: "Datos recibidos correctamente" });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: "Error inserting data" });
    }
});

// ✅ Start Server
const PORT = process.env.PORT || 8000;
app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));
