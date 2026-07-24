/**
 * صور Google تأتي كروابط كاملة (https://...)
 * أما الصور المرفوعة محليًا فتُخزَّن كمسار نسبي (/static/uploads/avatars/...)
 * من السيرفر، وتحتاج لإضافة عنوان الباك إند (origin) أمامها لتُعرض بشكل صحيح.
 */
const API_ORIGIN = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/api\/v1\/?$/, "");

export function resolveAvatarUrl(avatarUrl) {
  if (!avatarUrl) return null;
  if (avatarUrl.startsWith("http://") || avatarUrl.startsWith("https://")) {
    return avatarUrl;
  }
  return `${API_ORIGIN}${avatarUrl}`;
}
