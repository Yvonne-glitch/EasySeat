const mysql = require('mysql2/promise');
const fs = require('fs').promises;
const path = require('path');

async function initializeDatabase() {
    const connection = await mysql.createConnection({
        host: 'localhost',
        user: 'root',
        password: '123456'
    });

    try {
        // 读取SQL文件
        const sqlFile = await fs.readFile(path.join(__dirname, 'init-db.sql'), 'utf8');
        const statements = sqlFile.split(';').filter(stmt => stmt.trim());

        // 执行每个SQL语句
        for (let statement of statements) {
            if (statement.trim()) {
                await connection.execute(statement);
            }
        }

        console.log('数据库初始化成功！');
    } catch (error) {
        console.error('数据库初始化失败:', error);
    } finally {
        await connection.end();
    }
}

initializeDatabase();
