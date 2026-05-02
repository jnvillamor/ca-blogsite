/**
 * Utility functions to extract and format content previews from BlockNote content.
 */
import { BlockNoteContent } from "@/data-access/schemas/blogs.schema";

/**
 * Extract text from a single BlockNote block
 */
const extractTextFromBlock = (block: BlockNoteContent): string => {
  if (!block.content || !Array.isArray(block.content)) return '';

  return block.content
    .filter((item) => item.type === 'text' && typeof item.text === 'string')
    .map((item) => item.text)
    .join('')
}

/**
 * Extract preview text from BlockNote JSON content
 * @param content  - BlockNote content as JSON string
 * @param maxLength  - Maximum length of the preview text (default: 150)
 */
export const extractContentPreview = (
  blocks: BlockNoteContent[] | null,
  maxLength: number = 150
): string => {
  if (!blocks) return '';

  try {
    if (!Array.isArray(blocks) || blocks.length === 0) {
      return '';
    } 

    // Extract text from all blocks and concatenate
    const allText = blocks
      .map((block) => extractTextFromBlock(block))
      .filter((text) => text.trim().length > 0)
      .join(' ')
      .trim();
    
    if (allText.length === 0) 
      return 'No content yet.';
    
    return allText
  } catch (error) {
    console.error('Error parsing content for preview:', error);
    return 'Error loading content preview.';
  }
}

/**
 * Count total words in BlockNote content
 * Useful for displaying reading time or content statistics
 */
export function countContentWords(blocks: BlockNoteContent[] | null): number {
  if (!blocks) return 0

  try {
    if (!Array.isArray(blocks)) return 0

    const allText = blocks
      .map((block) => extractTextFromBlock(block))
      .join(' ')

    return allText.split(/\s+/).filter((word) => word.length > 0).length
  } catch (error) {
    console.error('[v0] Error counting words:', error)
    return 0
  }
}

/**
 * Calculate reading time from content
 * Based on average reading speed of 200 words per minute
 */
export function calculateReadingTime(
  blocks: BlockNoteContent[] | null
): { minutes: number; seconds: number } {
  const wordCount = countContentWords(blocks)
  const totalSeconds = (wordCount / 200) * 60

  return {
    minutes: Math.floor(totalSeconds / 60),
    seconds: Math.floor(totalSeconds % 60),
  }
}

/**
 * Format reading time as human-readable string
 */
export function formatReadingTime(
  blocks: BlockNoteContent[] | null
): string {
  const { minutes, seconds } = calculateReadingTime(blocks)

  if (minutes === 0) {
    return 'Less than 1 min read'
  }

  if (seconds > 30) {
    return `${minutes + 1} min read`
  }

  return `${minutes} min read`
}
