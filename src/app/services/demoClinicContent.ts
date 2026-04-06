export const demoClinicBrand = {
  name: "Lab Smile",
  subtitle: "центр эстетической стоматологии",
  logoLetter: "L",
  programName: "Lab Smile Bonus",
  city: "Алматы",
};

export const demoClinicContacts = {
  phoneDisplay: "+7 (775) 080-00-17",
  phoneHref: "+77750800017",
  email: "hello@labsmile.kz",
  whatsappUrl: "https://wa.me/77750800017",
  instagramUrl: "https://www.instagram.com/labsmile.kz/",
  instagramLabel: "@labsmile.kz",
  addressLine: "пр. Абая, 51/53",
  addressDetails: "Алматы, удобный подъезд и запись через WhatsApp или Instagram",
  mapNote: "Алматы · пр. Абая",
  schedule: [
    { days: "Понедельник — Пятница", hours: "09:00 — 20:00" },
    { days: "Суббота", hours: "10:00 — 18:00" },
    { days: "Воскресенье", hours: "по записи" },
  ],
};

export const publicPageContent = {
  heroTag: "Эстетика улыбки и понятный сервис",
  heroTitle: "Стоматология, где всё строится вокруг красивой улыбки и честного плана лечения",
  heroDescription:
    "Lab Smile — эстетическая стоматология в Алматы. Ортодонтия, виниры, реставрации, гигиена и мягкий сервис без скрытых платежей.",
  heroPrimaryCta: "Записаться на консультацию",
  heroSecondaryCta: "Войти в кабинет",
  features: [
    { icon: "shield", label: "Честная цена", sub: "Без скрытых доплат после консультации" },
    { icon: "star", label: "4.9 / 5", sub: "Оценка по открытым отзывам" },
    { icon: "clock", label: "09:00–20:00", sub: "Рабочий график в будни" },
    { icon: "smile", label: "Эстетика улыбки", sub: "Брекеты, виниры, отбеливание" },
  ],
  quickNav: [
    { label: "Услуги", sub: "Ортодонтия, эстетика, терапия", page: "services", icon: "🦷" },
    { label: "Команда", sub: "Специалисты по эстетике улыбки", page: "doctors", icon: "👩‍⚕️" },
    { label: "Цены", sub: "Понятные диапазоны в тенге", page: "prices", icon: "💳" },
    { label: "Контакты", sub: "Алматы, WhatsApp и Instagram", page: "contacts", icon: "📍" },
  ],
  authBenefits: [
    "Онлайн-запись на консультацию",
    "История визитов и оплат",
    "Бонусная программа",
    "Напоминания и подтверждения",
  ],
};

export const serviceCategories = [
  { id: "all", label: "Все услуги" },
  { id: "diagnostics", label: "Диагностика" },
  { id: "hygiene", label: "Гигиена" },
  { id: "treatment", label: "Лечение" },
  { id: "ortho", label: "Ортодонтия" },
  { id: "aesthetics", label: "Эстетика" },
];

export const clinicServices = [
  {
    id: 1,
    category: "diagnostics",
    icon: "💬",
    name: "Первичная консультация",
    desc: "Осмотр, фотопротокол, разбор жалоб и спокойное объяснение вариантов лечения без давления.",
    price: "от 10 000 ₸",
    duration: "30–40 мин",
    tags: ["Диагностика", "План лечения"],
  },
  {
    id: 2,
    category: "diagnostics",
    icon: "📸",
    name: "Диагностика улыбки",
    desc: "Подбор эстетического решения: виниры, реставрации, отбеливание или ортодонтия, если нужна коррекция прикуса.",
    price: "от 15 000 ₸",
    duration: "40 мин",
    tags: ["Эстетика", "Фото-анализ"],
  },
  {
    id: 3,
    category: "hygiene",
    icon: "✨",
    name: "Профессиональная гигиена",
    desc: "Комплексная чистка, снятие налёта и полировка, чтобы подготовить улыбку к лечению или поддерживать результат.",
    price: "от 25 000 ₸",
    duration: "60 мин",
    tags: ["Гигиена", "Профилактика"],
  },
  {
    id: 4,
    category: "treatment",
    icon: "🔬",
    name: "Лечение кариеса",
    desc: "Аккуратное восстановление зуба с упором на эстетику, форму и естественный оттенок эмали.",
    price: "от 25 000 ₸",
    duration: "60–90 мин",
    tags: ["Терапия", "Эстетика"],
  },
  {
    id: 5,
    category: "treatment",
    icon: "🧩",
    name: "Художественная реставрация",
    desc: "Восстановление сколов, формы и цвета передней группы зубов, когда важен визуальный результат.",
    price: "от 35 000 ₸",
    duration: "60–90 мин",
    tags: ["Реставрация", "Передние зубы"],
  },
  {
    id: 6,
    category: "ortho",
    icon: "😁",
    name: "Брекет-система",
    desc: "Пошаговое исправление прикуса с понятным маршрутом лечения, контролем сроков и регулярными осмотрами.",
    price: "от 350 000 ₸",
    duration: "от 12 мес",
    tags: ["Ортодонтия", "Прикус"],
  },
  {
    id: 7,
    category: "ortho",
    icon: "🫧",
    name: "Элайнеры",
    desc: "Прозрачный путь к выравниванию зубов для тех, кто хочет аккуратную коррекцию без выраженной конструкции.",
    price: "от 1 500 000 ₸",
    duration: "от 10 мес",
    tags: ["Ортодонтия", "Незаметно"],
  },
  {
    id: 8,
    category: "aesthetics",
    icon: "💎",
    name: "Керамические виниры",
    desc: "Создание новой формы и оттенка улыбки для пациентов, которым важен заметный, но естественный эстетический результат.",
    price: "от 120 000 ₸",
    duration: "2–3 визита",
    tags: ["Виниры", "Улыбка"],
  },
  {
    id: 9,
    category: "aesthetics",
    icon: "🌟",
    name: "Отбеливание",
    desc: "Профессиональное осветление эмали с бережным протоколом и рекомендациями по сохранению результата.",
    price: "от 90 000 ₸",
    duration: "90 мин",
    tags: ["Эстетика", "Быстрый результат"],
  },
];

export const serviceAdvantages = [
  {
    title: "Честная стоимость",
    desc: "Мы показываем диапазоны заранее и обсуждаем план лечения до старта, чтобы не было сюрпризов на оплате.",
  },
  {
    title: "Эстетический фокус",
    desc: "Каждое решение оценивается не только по функции, но и по тому, как оно будет выглядеть в улыбке.",
  },
  {
    title: "Удобная коммуникация",
    desc: "Пациент получает понятные объяснения, этапы лечения и быстрый контакт через WhatsApp или Instagram.",
  },
  {
    title: "Ортодонтия и smile design",
    desc: "Работаем там, где важен путь к красивой улыбке: брекеты, элайнеры, виниры, реставрации.",
  },
  {
    title: "Комфортный ритм визитов",
    desc: "Запись, подтверждения и follow-up выстроены так, чтобы лечение не разваливалось между визитами.",
  },
  {
    title: "Понятный личный кабинет",
    desc: "Пациент видит визиты, оплаты, бонусы и историю без звонков в регистратуру.",
  },
];

export const clinicDoctors = [
  {
    id: 1,
    name: "Аружан Сейтова",
    role: "Ортодонт",
    experience: "10 лет",
    rating: 4.9,
    reviews: 86,
    photo:
      "https://images.unsplash.com/photo-1734002886107-168181bcd6a1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmZW1hbGUlMjBkb2N0b3IlMjBzbWlsaW5nJTIwbWVkaWNhbCUyMHByb2Zlc3Npb25hbHxlbnwxfHx8fDE3NzQ5NTYzNzV8MA&ixlib=rb-4.1.0&q=80&w=400",
    desc: "Ведет пациентов с брекетами и элайнерами, умеет собирать план лечения так, чтобы он был понятен и реалистичен по срокам.",
    education: "КазНМУ, ординатура по ортодонтии",
    specialties: ["Брекеты", "Элайнеры", "Прикус"],
  },
  {
    id: 2,
    name: "Диана Мусина",
    role: "Стоматолог-терапевт, эстетист",
    experience: "8 лет",
    rating: 4.9,
    reviews: 71,
    photo:
      "https://images.unsplash.com/photo-1753487050317-919a2b26a6ed?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx3b21hbiUyMGh5Z2llbmlzdCUyMGRlbnRhbCUyMGNsaW5pYyUyMHdoaXRlJTIwdW5pZm9ybXxlbnwxfHx8fDE3NzQ5NTYzODl8MA&ixlib=rb-4.1.0&q=80&w=400",
    desc: "Работает с кариесом, художественными реставрациями и отбеливанием, когда пациенту важны и здоровье, и визуальный результат.",
    education: "КМУ, терапевтическая стоматология",
    specialties: ["Кариес", "Реставрации", "Отбеливание"],
  },
  {
    id: 3,
    name: "Еркебулан Жаксылыков",
    role: "Ортопед, smile design",
    experience: "11 лет",
    rating: 4.8,
    reviews: 63,
    photo:
      "https://images.unsplash.com/photo-1588776814546-daab30f310ce?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkZW50aXN0JTIwZG9jdG9yJTIwcHJvZmVzc2lvbmFsJTIwcG9ydHJhaXQlMjB3aGl0ZSUyMGNvYXR8ZW58MXx8fHwxNzc0OTU2MzcwfDA&ixlib=rb-4.1.0&q=80&w=400",
    desc: "Собирает эстетические кейсы с винирами и коронками, когда пациент хочет спокойный и продуманный результат по форме и оттенку улыбки.",
    education: "КазНМУ, ортопедическая стоматология",
    specialties: ["Виниры", "Коронки", "Smile design"],
  },
  {
    id: 4,
    name: "Меруерт Абилова",
    role: "Гигиенист",
    experience: "6 лет",
    rating: 5.0,
    reviews: 58,
    photo:
      "https://images.unsplash.com/photo-1631596577204-53ad0d6e6978?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtYWxlJTIwb3J0aG9kb250aXN0JTIwZGVudGFsJTIwc3VyZ2VvbiUyMHBvcnRyYWl0fGVufDF8fHx8MTc3NDk1NjM3NXww&ixlib=rb-4.1.0&q=80&w=400",
    desc: "Отвечает за профессиональную гигиену и профилактику, чтобы улыбка выглядела ухоженно и лечение держалось дольше.",
    education: "Сертификация по профилактической стоматологии",
    specialties: ["Профгигиена", "Air Flow", "Профилактика"],
  },
];

export const doctorStats = [
  { value: "4", label: "ключевых направления" },
  { value: "1", label: "понятный маршрут лечения" },
  { value: "0", label: "скрытых доплат в плане" },
];

export const priceCategories = [
  {
    id: "diagnostics",
    label: "Диагностика и консультация",
    icon: "💬",
    items: [
      { name: "Первичная консультация", price: "10 000 ₸", note: "осмотр и план лечения" },
      { name: "Диагностика улыбки", price: "15 000 ₸", note: "для эстетических кейсов" },
      { name: "Повторный осмотр", price: "от 8 000 ₸", note: "" },
    ],
  },
  {
    id: "hygiene",
    label: "Гигиена",
    icon: "✨",
    items: [
      { name: "Профессиональная гигиена", price: "25 000 – 40 000 ₸", note: "" },
      { name: "Полировка и рекомендации по уходу", price: "включено", note: "" },
      { name: "Профилактический контроль", price: "от 8 000 ₸", note: "" },
    ],
  },
  {
    id: "treatment",
    label: "Лечение и реставрация",
    icon: "🔬",
    items: [
      { name: "Лечение кариеса", price: "25 000 – 60 000 ₸", note: "в зависимости от объема" },
      { name: "Художественная реставрация", price: "35 000 – 70 000 ₸", note: "" },
      { name: "Повторная терапевтическая консультация", price: "от 8 000 ₸", note: "" },
    ],
  },
  {
    id: "ortho",
    label: "Ортодонтия",
    icon: "😁",
    items: [
      { name: "Консультация ортодонта", price: "от 10 000 ₸", note: "" },
      { name: "Брекет-система", price: "от 350 000 ₸", note: "за старт лечения" },
      { name: "Элайнеры", price: "от 1 500 000 ₸", note: "после диагностики" },
      { name: "Контрольный визит", price: "от 20 000 ₸", note: "" },
    ],
  },
  {
    id: "aesthetics",
    label: "Эстетика улыбки",
    icon: "💎",
    items: [
      { name: "Отбеливание", price: "от 90 000 ₸", note: "" },
      { name: "Керамический винир", price: "от 120 000 ₸", note: "за единицу" },
      { name: "Консультация по smile design", price: "от 15 000 ₸", note: "" },
    ],
  },
];

export const bookingServices = [
  { id: "consult", name: "Первичная консультация", price: "10 000 ₸", duration: "30 мин", icon: "💬" },
  { id: "hygiene", name: "Профессиональная гигиена", price: "от 25 000 ₸", duration: "60 мин", icon: "✨" },
  { id: "caries", name: "Лечение кариеса", price: "от 25 000 ₸", duration: "60 мин", icon: "🔬" },
  { id: "whitening", name: "Отбеливание", price: "от 90 000 ₸", duration: "90 мин", icon: "🌟" },
  { id: "ortho", name: "Консультация ортодонта", price: "от 10 000 ₸", duration: "40 мин", icon: "😁" },
  { id: "veneers", name: "Консультация по винирам", price: "от 15 000 ₸", duration: "40 мин", icon: "💎" },
];

export const bookingDoctors = clinicDoctors.map((doctor) => ({
  id: doctor.id,
  name: doctor.name,
  role: doctor.role,
  available: true,
}));

export const staffLoginContent = {
  emailPlaceholder: "team@labsmile.kz",
};
