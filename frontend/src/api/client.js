import axios from "axios";

const client = axios.create({
  baseURL: "/api",
});

export const fetchSchedule = async () => {
  const { data } = await client.get("/schedule");
  return data;
};

export const fetchInventory = async () => {
  const { data } = await client.get("/inventory");
  return data;
};

export const fetchMachines = async () => {
  const { data } = await client.get("/machines");
  return data;
};

export const postOwnerQuery = async (payload) => {
  const { data } = await client.post("/query", payload);
  return data;
};
