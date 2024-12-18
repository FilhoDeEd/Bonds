const BASE_URL = "http://localhost:8000";
const ACCOUNT_URL = `${BASE_URL}/account`;
const USER_PROFILE_URL = `${BASE_URL}/user_profile`;
const FORUM_URL = `${BASE_URL}/forum`

// Endpoints centralizados
export const ENDPOINTS = {
  REGISTER: `${ACCOUNT_URL}/register/`,
  LOGIN: `${ACCOUNT_URL}/login/`,
  DETAIL: `${ACCOUNT_URL}/detail/`,

  EDIT: `${ACCOUNT_URL}/update/`,
  EDIT_NEIGHBORHOOD: `${ACCOUNT_URL}/update-neighborhood/`,
  EDIT_EMAIL: `${ACCOUNT_URL}/update-email/`,
  EDIT_PASSWORD: `${ACCOUNT_URL}/update-password/`,

  DELETE_ACCOUNT: `${ACCOUNT_URL}/anonymize/`,

  REFRESH: `${ACCOUNT_URL}/refresh`,
  STATES: `${USER_PROFILE_URL}/states`,
  CITIES: `${USER_PROFILE_URL}/cities`,
  NEIGHBORHOODS:`${USER_PROFILE_URL}/neighborhoods`,

  LIST_FORUNS: `${FORUM_URL}/list/`,
  FORUM_DETAIL: `${FORUM_URL}/detail`,
  REGISTER_FORUM: `${FORUM_URL}/register/`,
};