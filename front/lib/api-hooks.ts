import useSWR from 'swr';
import { fetcher } from './api-config';

export const useProjects = () => {
  return useSWR('/api/buildings', fetcher);
};

export const useProject = (id: string) => {
  return useSWR(id ? `/api/buildings/${id}` : null, fetcher);
};

export const useDevelopers = () => {
  return useSWR('/api/developers', fetcher);
};

export const useCategories = () => {
  return useSWR('/api/building-classes', fetcher);
};

export const useProjectReviews = (projectId: string) => {
  return useSWR(projectId ? `/api/buildings/${projectId}/reviews` : null, fetcher);
};

export const useFeaturedProjects = () => {
  return useSWR('/api/buildings/featured', fetcher);
}; 