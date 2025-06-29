const express = require('express');
const session = require('express-session');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 4000;







// Настройка сессий
app.use(session({
  secret: 'my_secret_key_123',
  resave: false,
  saveUninitialized: true
}));

// Обработка формы
app.use(express.urlencoded({ extended: true }));

// ➤ Переход на /login, если не авторизован
app.get('/', (req, res) => {
  if (req.session.loggedIn) {
    return res.redirect('/home');
  }
  res.redirect('/login');
});

// ➤ Страница логина
app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

// ➤ Проверка логина
app.post('/login', (req, res) => {
  const { username, password } = req.body;

  if (username === 'admin' && password === '1234') {
    req.session.loggedIn = true;
    return res.redirect('/home');
  }

  res.send('<h3>❌ Invalid credentials. <a href="/login">Try again</a></h3>');
});

// ➤ Главная (только если вошёл)
app.get('/home', (req, res) => {
  if (!req.session.loggedIn) {
    return res.redirect('/login');
  }
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// ➤ Картинка (только если вошёл)
app.get('/frame.jpg', (req, res) => {
  if (!req.session.loggedIn) {
    return res.status(403).send('Forbidden');
  }
  res.sendFile(path.join(__dirname, 'public', 'frame.jpg'));
});

// ➤ Стиль (не защищаем)
app.get('/style.css', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'style.css'));
});

// ➤ API: количество машин
app.get('/count', (req, res) => {
  if (!req.session.loggedIn) return res.status(401).json({ error: 'Unauthorized' });

  fs.readFile('data/count.txt', 'utf8', (err, data) => {
    if (err) return res.json({ count: 0 });
    res.json({ count: parseInt(data) });
  });
});

// ➤ Выход
app.get('/logout', (req, res) => {
  req.session.destroy(() => {
    res.redirect('/login');
  });
});

// Запуск сервера
app.listen(PORT, () => {
  console.log(`🔐 Secure server running at http://localhost:${PORT}`);
});








// Static fayllarni xizmat qilish
app.use(express.static(path.join(__dirname, 'public')));

// Sahifalarni render qilish
app.get('/home', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'home.html'));
});

app.get('/statistics', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'statistics.html'));
});

// Boshqa sahifalar uchun ham shu tarzda yo'llar qo'shish
app.listen(3000, () => {
    console.log('Server ishlamoqda...');
});