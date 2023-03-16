from abc import ABC, abstractstaticmethod


class Sort(ABC):
    @abstractstaticmethod
    def sort():
        pass


class QuickSort(Sort):
    def sort():
        print("I'm Quick sort")


class ExternalSort(Sort):
    def sort():
        print("I'm External sort")


class ConcurrentExternalSort(Sort):
    def sort():
        print("I'm ConcurrentExternal sort")


class MapReduceSort(Sort):
    def sort():
        print("I'm MapReduce sort")


class SortAlgFactory:
    sort_algs = {}

    def __init__(self):
        self.sort_algs['QuickSort'] = QuickSort()
        self.sort_algs['ExternalSort'] = ExternalSort()
        self.sort_algs['ConcurrentExternalSort'] = ConcurrentExternalSort()
        self.sort_algs['MapReduceSort'] = MapReduceSort()

    @classmethod
    def getSortAlg(cls, sort_type):
        if (sort_type is None or sort_type not in cls.sort_algs.keys()):
            raise RuntimeError('sort_type is error')

        return cls.sort_algs.get(sort_type)


'''
public class Sorter { 
    private static final long GB = 1000 * 1000 * 1000; 
    public void sortFile(String filePath) { 
        // 省略校验逻辑 
        File file = new File(filePath); 
        long fileSize = file.length(); 
        ISortAlg sortAlg; 
        if (fileSize < 6 * GB) { 
            // [0, 6GB) sortAlg = new QuickSort(); 
        } else if (fileSize < 10 * GB) { 
            // [6GB, 10GB) sortAlg = new ExternalSort(); } 
        else if (fileSize < 100 * GB) { 
            // [10GB, 100GB) 
            sortAlg = new ConcurrentExternalSort(); } 
        else { 
            // [100GB, ~) 
            sortAlg = new MapReduceSort(); } 
        sortAlg.sort(filePath); 
    }
}
'''

'''
public class Sorter {
    private static final long GB = 1000 * 1000 * 1000;
    private static final List<AlgRange> algs = new ArrayList<>();
    static {
        algs.add(new AlgRange(0, 6*GB, SortAlgFactory.getSortAlg("QuickSort")));
        algs.add(new AlgRange(6*GB, 10*GB, SortAlgFactory.getSortAlg("ExternalSort")));
        algs.add(new AlgRange(10*GB, 100*GB, SortAlgFactory.getSortAlg("ConcurrentExternalSort")));
        algs.add(new AlgRange(100*GB, Long.MAX_VALUE, SortAlgFactory.getSortAlg("MapReduceSort")));
    }

    public void sortFile(String filePath) {
        // 省略校验逻辑
        File file = new File(filePath);
        long fileSize = file.length();
        ISortAlg sortAlg = null;
        for (AlgRange algRange : algs) {
            if (algRange.inRange(fileSize)) {
                sortAlg = algRange.getAlg();
                break;
            }
        }
        sortAlg.sort(filePath);
    }

    private static class AlgRange {
        private long start;
        private long end;
        private ISortAlg alg;

        public AlgRange(long start, long end, ISortAlg alg) {
            this.start = start;
            this.end = end;
            this.alg = alg;
        }

        public ISortAlg getAlg() {
            return alg;
        }

        public boolean inRange(long size) {
            return size >= start && size < end;
        }
    }
}
'''
