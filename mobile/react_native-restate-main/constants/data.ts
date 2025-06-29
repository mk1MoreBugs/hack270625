import icons from "./icons";
import images from "./images";
import { projectsData, recommendedApartmentsData } from "../lib/data";

export const cards = recommendedApartmentsData.map((apartment, index) => ({
  title: apartment.name,
  location: apartment.project,
  price: apartment.price,
  rating: 4.8 - index * 0.2,
  category: apartment.rooms === 0 ? "студия" : "квартира",
  image: apartment.image,
}));

export const featuredCards = projectsData.slice(0, 2).map((project) => ({
  title: project.name,
  location: project.location,
  price: project.price,
  rating: project.rating,
  image: project.image,
  category: project.class.toLowerCase(),
}));

export const categories = [
  { title: "Все", category: "All" },
  { title: "Дома", category: "House" },
  { title: "Кондо", category: "Condos" },
  { title: "Дуплексы", category: "Duplexes" },
  { title: "Студии", category: "Studios" },
  { title: "Виллы", category: "Villa" },
  { title: "Квартиры", category: "Apartments" },
  { title: "Таунхаусы", category: "Townhomes" },
  { title: "Другое", category: "Others" },
];

export const settings = [
  {
    title: "Мои бронирования",
    icon: icons.calendar,
  },
  {
    title: "Платежи",
    icon: icons.wallet,
  },
  {
    title: "Профиль",
    icon: icons.person,
  },
  {
    title: "Уведомления",
    icon: icons.bell,
  },
  {
    title: "Безопасность",
    icon: icons.shield,
  },
  {
    title: "Язык",
    icon: icons.language,
  },
  {
    title: "Центр помощи",
    icon: icons.info,
  },
  {
    title: "Пригласить друзей",
    icon: icons.people,
  },
];

export const facilities = [
  {
    title: "Прачечная",
    icon: icons.laundry,
  },
  {
    title: "Парковка",
    icon: icons.carPark,
  },
  {
    title: "Спортивный центр",
    icon: icons.run,
  },
  {
    title: "Кухня",
    icon: icons.cutlery,
  },
  {
    title: "Спортзал",
    icon: icons.dumbell,
  },
  {
    title: "Бассейн",
    icon: icons.swim,
  },
  {
    title: "Wi-Fi",
    icon: icons.wifi,
  },
  {
    title: "Зооцентр",
    icon: icons.dog,
  },
];

export const gallery = [
  {
    id: 1,
    image: images.newYork,
  },
  {
    id: 2,
    image: images.japan,
  },
  {
    id: 3,
    image: images.newYork,
  },
  {
    id: 4,
    image: images.japan,
  },
  {
    id: 5,
    image: images.newYork,
  },
  {
    id: 6,
    image: images.japan,
  },
];
