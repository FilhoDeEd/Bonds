const API_URL = process.env.VUE_APP_API_URL || "http://localhost:8000";
const ACCOUNT_URL = `${API_URL}/account`;
const USER_PROFILE_URL = `${API_URL}/user_profile`;
const FORUM_URL = `${API_URL}/forum`;
const EVENT_URL = `${FORUM_URL}/event`;
const COMMENT_URL = `${API_URL}/comment`;
const REPORT_URL = `${COMMENT_URL}/report`;

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
  EDIT_FORUM: `${FORUM_URL}/edit`,
  SUBSCRIBE_FORUM: `${FORUM_URL}/subscribe`,
  UNSUBSCRIBE_FORUM: `${FORUM_URL}/unsubscribe`,

  LIST_EVENTS: `${EVENT_URL}/list/`,
  EVENT_DETAIL: `${EVENT_URL}/detail`,
  REGISTER_EVENT: `${EVENT_URL}/register/`,
  EDIT_EVENT: `${EVENT_URL}/edit`,
  REVIEW_EVENT: `${FORUM_URL}/review/register/`,

  LIST_COMMENTS : `${COMMENT_URL}/list`,
  CREATE_COMMENT : `${COMMENT_URL}/register/`,
  EDIT_COMMENT : `${COMMENT_URL}/edit`,
  DELETE_COMMENT : `${COMMENT_URL}/delete`,
  LIKE_COMMENT: `${COMMENT_URL}/like/`,
  DISLIKE_COMMENT: `${COMMENT_URL}/dislike/`,
  UNLIKE_COMMENT: `${COMMENT_URL}/unlike/`,

  REGISTER_REPORT: `${REPORT_URL}/register/`,
  REPORT_EDIT: `${REPORT_URL}/edit`,
  REPORT_DELETE: `${REPORT_URL}/delete`,


};
