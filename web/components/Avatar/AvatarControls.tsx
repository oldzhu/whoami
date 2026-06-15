'use client';

interface AvatarControlsProps {
  onUploadPhoto: () => void;
  photoUrl?: string;
}

export function AvatarControls({ onUploadPhoto, photoUrl }: AvatarControlsProps) {
  return (
    <div className="flex gap-2 text-sm">
      <button onClick={onUploadPhoto} className="px-3 py-1 bg-gray-100 rounded hover:bg-gray-200">
        {photoUrl ? 'Change Photo' : 'Upload Photo'}
      </button>
    </div>
  );
}
