import heapq

from run_util import run_puzzle


class Disk:
    def __init__(self, data: str):
        digits = list(map(int, data.strip()))
        self.files = []
        self.disk = {}
        self._free_map = {}
        self._end_map = {}
        self._heaps = {size: [] for size in range(1, 10)}

        current_index = 0
        current_file_id = 0
        for i, segment_length in enumerate(digits):
            if i % 2 == 0:
                if segment_length > 0:
                    self.files.append((current_index, segment_length, current_file_id))
                    current_index += segment_length
                    current_file_id += 1
            else:
                if segment_length > 0:
                    self._add_segment(current_index, segment_length)
                current_index += segment_length

        for file_start, file_length, file_id in self.files:
            for offset in range(file_length):
                self.disk[file_start + offset] = file_id

        for segment_start, (seg_start, seg_len) in self._free_map.items():
            for offset in range(seg_len):
                self.disk.setdefault(seg_start + offset, None)

    def checksum(self) -> int:
        return sum(pos * fid for pos, fid in self.disk.items() if fid is not None)

    def _add_segment(self, start: int, length: int):
        if length <= 0:
            return
        seg_start, seg_len = start, length
        end_pos = seg_start + seg_len

        if seg_start in self._end_map:
            left_start = self._end_map.pop(seg_start)
            left_seg_start, left_seg_len = self._free_map.pop(left_start)
            seg_start = left_start
            seg_len += left_seg_len
            end_pos = seg_start + seg_len

        if end_pos in self._free_map:
            right_seg_start, right_seg_len = self._free_map.pop(end_pos)
            self._end_map.pop(end_pos + right_seg_len, None)
            seg_len += right_seg_len
            end_pos = seg_start + seg_len

        self._free_map[seg_start] = (seg_start, seg_len)
        self._end_map[end_pos] = seg_start

        for size in range(1, min(9, seg_len) + 1):
            heapq.heappush(self._heaps[size], (seg_start, seg_len))

    def _remove_segment(self, segment_start: int):
        segment = self._free_map.pop(segment_start, None)
        if segment is not None:
            seg_end = segment_start + segment[1]
            self._end_map.pop(seg_end, None)
        return segment

    def _split_segment(self, segment_start: int, segment_length: int, new_start: int, used_length: int):
        self._remove_segment(segment_start)
        leftover_size = new_start - segment_start
        if leftover_size > 0:
            self._add_segment(segment_start, leftover_size)

        used_end = new_start + used_length
        right_size = (segment_start + segment_length) - used_end
        if right_size > 0:
            self._add_segment(used_end, right_size)

    def _find_suitable_segment(self, file_start: int, file_length: int):
        heap = self._heaps[file_length]
        while heap:
            seg_start, seg_len = heap[0]
            current_segment = self._free_map.get(seg_start)
            if current_segment is None or current_segment[1] < file_length or seg_start >= file_start:
                heapq.heappop(heap)
            else:
                return seg_start, seg_len
        return None

    def defragment_block(self):
        if not self.disk:
            return
        left = 0
        right = max(self.disk)
        while left < right:
            if self.disk.get(right) is not None:
                file_id = self.disk[right]
                self.disk[right] = None
                while self.disk.get(left) is not None:
                    left += 1
                self.disk[left] = file_id
            right -= 1

    def defragment_file(self):
        for file_start, file_length, file_id in sorted(self.files, key=lambda x: x[2], reverse=True):
            result = self._find_suitable_segment(file_start, file_length)
            if result is not None:
                seg_start, seg_len = result
                self._split_segment(seg_start, seg_len, seg_start, file_length)
                for offset in range(file_length):
                    self.disk[seg_start + offset] = file_id
                self._add_segment(file_start, file_length)
                for offset in range(file_length):
                    self.disk[file_start + offset] = None


def part_a(data: str) -> int:
    d = Disk(data)
    d.defragment_block()
    return d.checksum()


def part_b(data: str) -> int:
    d = Disk(data)
    d.defragment_file()
    return d.checksum()


def main():
    examples = [
        ("2333133121414131402", 1928, 2858),
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
