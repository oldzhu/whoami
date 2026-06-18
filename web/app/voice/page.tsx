'use client';
import { useI18n } from '@/lib/i18n';

export default function VoicePage() {
  const { t } = useI18n();
  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">{t('voice.title')}</h2>
      <div className="bg-white rounded-lg p-6 shadow min-h-[400px] flex items-center justify-center text-gray-400">
        {t('voice.coming')}
      </div>
    </div>
  );
}
