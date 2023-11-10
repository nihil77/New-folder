const db = require('./db'); // Import the database connection

module.exports = {
  registerUser: async (username, password) => {
    const query = 'INSERT INTO users (username, password) VALUES (?, ?)';
    const [results] = await db.promise().query(query, [username, password]);
    return results.insertId;
  },

  findUserByUsername: async (username) => {
    const query = 'SELECT * FROM users WHERE username = ?';
    const [results] = await db.promise().query(query, [username]);
    return results[0];
  },

  findUserById: async (userId) => {
    const query = 'SELECT * FROM users WHERE id = ?';
    const [results] = await db.promise().query(query, [userId]);
    return results[0];
  },

  createSession: async (userId, sessionToken) => {
    const query = 'INSERT INTO sessions (user_id, session_token) VALUES (?, ?)';
    const [results] = await db.promise().query(query, [userId, sessionToken]);
    return results.insertId;
  },

  findSessionByToken: async (sessionToken) => {
    const query = 'SELECT * FROM sessions WHERE session_token = ?';
    const [results] = await db.promise().query(query, [sessionToken]);
    return results[0];
  },
};
