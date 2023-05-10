import React, { useState } from 'react';
import axios from 'axios';
import Link from 'next/link';
import Layout from '@/components/layout';

const DocumentUpload: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [documentId, setDocumentId] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!selectedFile) {
      setUploadStatus('Please select a file.');
      return;
    }

    setIsLoading(true);

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('file_name', selectedFile.name);
    formData.append('file_size', selectedFile.size.toString());
    formData.append('content_type', selectedFile.type);

    try {
      const response = await axios.post('http://localhost:8000/doc_parse/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const document = response.data.file_id;

      localStorage.setItem('documentId', document);

      if (response.status === 201) {
        
        setUploadStatus('File uploaded successfully.');
      } else if (response.status === 200) {
        setUploadStatus('File already exists.');
      }
    } catch (error: any) {
      if (error.response && error.response.status === 400) {
        setUploadStatus('Error: Unsupported file type or invalid data.');
      } else {
        setUploadStatus('Error: Unable to upload file.');
      }
    } finally {
        setIsLoading(false);
    }
  };

  return (

    <Layout>
          
    <div className="govuk-width-container">
      <div className="govuk-grid-row">
        <div className="govuk-grid-column-two-thirds">
          <h1 className="govuk-heading-l">Document Upload</h1>
          <form onSubmit={handleSubmit} className="govuk-!-mt-r6">
            <div className="govuk-form-group">
              <input
                className="govuk-file-upload"
                id="file-upload"
                name="file-upload"
                type="file"
                onChange={handleFileChange}
              />
            </div>
            <button
              className="govuk-button"
              data-module="govuk-button"
              type="submit"
              disabled={isLoading}
            >
              {isLoading ? 'Uploading...' : 'Upload'}
            </button>
          </form>
          {uploadStatus && (
            <p className="govuk-body govuk-!-mt-r4">{uploadStatus}</p>
          )}
          {uploadStatus === 'File uploaded successfully.' && (
            <Link href="/chat">
              <div className='govuk-link'>
                Go to Chat
              </div>
            </Link>
          )}
        </div>
      </div>
    </div>

    </Layout>
 
  );
};

export default DocumentUpload;
