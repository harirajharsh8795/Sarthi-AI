import re
import logging

logger = logging.getLogger("saarthi.compression")

class CompressionService:
    """
    Deduplicates and compresses context chunks before sending them to the LLM.
    Reduces prompt length and improves generation speeds.
    """

    def find_overlap(self, s1: str, s2: str, min_overlap: int = 15) -> int:
        """Finds overlap length between end of s1 and start of s2."""
        s1_len = len(s1)
        s2_len = len(s2)
        max_check = min(s1_len, s2_len)
        
        for length in range(max_check, min_overlap - 1, -1):
            if s1[s1_len - length:] == s2[:length]:
                return length
        return 0

    def compress_context(self, chunks: list) -> dict:
        """
        Compresses neighboring text chunks from the same document page.
        Returns: {
            "compressed_chunks": list, 
            "original_chars": int, 
            "compressed_chars": int, 
            "ratio": float
        }
        """
        if not chunks:
            return {
                "compressed_chunks": [],
                "original_chars": 0,
                "compressed_chars": 0,
                "ratio": 1.0
            }

        original_chars = sum(len(c["text"]) for c in chunks)
        
        # Group chunks by source & page_number
        grouped = {}
        for c in chunks:
            key = f"{c['source']}_p{c['page_number']}"
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(c)

        compressed_chunks = []
        
        for key, page_chunks in grouped.items():
            if not page_chunks:
                continue
                
            # Sort page chunks by index or similarity score
            page_chunks.sort(key=lambda x: x.get("hybrid_score", 0.0), reverse=True)
            
            # Start merging
            merged_text = page_chunks[0]["text"]
            merged_meta = dict(page_chunks[0])
            
            # Record citation indices mapped to this merge block
            citation_indices = {merged_meta.get("index", 1)}
            
            for next_chunk in page_chunks[1:]:
                next_text = next_chunk["text"]
                citation_indices.add(next_chunk.get("index", 1))
                
                # Check overlap at end of merged_text and start of next_text
                overlap_len = self.find_overlap(merged_text, next_text)
                
                if overlap_len > 0:
                    merged_text += next_text[overlap_len:]
                else:
                    # check inverse overlap (next_text end overlaps merged_text start)
                    inv_overlap = self.find_overlap(next_text, merged_text)
                    if inv_overlap > 0:
                        merged_text = next_text + merged_text[inv_overlap:]
                    else:
                        # Simple concat separated by space if no overlap
                        merged_text += " " + next_text
                        
            merged_meta["text"] = merged_text
            # Keep citation indices in metadata
            merged_meta["citation_indices"] = sorted(list(citation_indices))
            compressed_chunks.append(merged_meta)
            
        compressed_chars = sum(len(c["text"]) for c in compressed_chunks)
        ratio = compressed_chars / original_chars if original_chars > 0 else 1.0
        
        logger.info(
            f"Context compressed: original={original_chars} chars, "
            f"compressed={compressed_chars} chars, ratio={ratio:.2f}"
        )
        
        return {
            "compressed_chunks": compressed_chunks,
            "original_chars": original_chars,
            "compressed_chars": compressed_chars,
            "ratio": round(ratio, 4)
        }

compression_service = CompressionService()
