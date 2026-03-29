export interface UploadedFile {
  name: string;
  status: 'uploading' | 'uploaded' | 'deleting';
}
