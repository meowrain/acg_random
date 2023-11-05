# ArrayList实现
```java
import java.util.NoSuchElementException;

public class MyArrayList<E> {
    // 存储数据得数组
    private E[] data;
    // 记录数组中元素得个数
    private int size;
    // 设置初始容量
    private static final int CAPACITY = 10;

    public MyArrayList() {
        this.data = (E[]) new Object[CAPACITY];
        this.size = 0;
    }

    public MyArrayList(int initCapacity) {
        this.data = (E[]) new Object[initCapacity];
        this.size = 0;
    }

    /* 增 */
    public void addLast(E e) {
        if (data.length == size) { // 大小不够就扩容
            resize(data.length * 2);
        }
        data[size] = e;
        size++;
    }

    // 在index索引位置添加一个元素element
    public void add(int index, E element) { // 大小不够就扩容
        checkPositionIndex(index); // 检查index索引位置是否可以添加元素
        if (data.length == size) {
            resize(data.length * 2);
        }
        for (int i = size; i < index; i--) { // 先移动位置
            data[i] = data[i - 1];
        }
        data[index] = element;
        size++;

    }

    /* 删除 */
    // 移除数组中最后一个元素并返回
    public E removeLast() {
        if (isEmpty()) {
            throw new NoSuchElementException();
        }
        if (size < data.length / 4) { // 如果数组元素个数小于了数组的四分之一，那么就缩容，防止占用太多内存
            resize(data.length / 2);
        }
        E temp = data[size - 1]; // 存储要被删除的元素，以供后面返回
        data[size - 1] = null; // 必须置空，才能让GC回收
        size--;
        return temp;
    }

    // 删除index对应的元素并返回
    public E remove(int index) {
        checkElementIndex(index);
        E temp = data[index];
        for (int i = index; i < size; i++) {
            data[i] = data[i + 1];
        }
        size--;
        return temp;
    }

    /* 改 */
    // 把索引为index的元素改为element并返回原来的元素
    public E set(int index, E element) {
        checkElementIndex(index);
        E temp = data[index]; // 存储没改的时候的元素，以供后面返回
        data[index] = element;
        return temp;
    }

    /* 查 */
    // 返回索引位置index的元素
    public E get(int index) {
        checkElementIndex(index);
        return data[index];
    }

    /* 主要函数 */
    public int size() {
        return size;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    /* 私有函数 */
    private boolean isElementIndex(int index) {
        return index >= 0 && index < size;
    }

    private boolean isPositionIndex(int index) {
        return index >= 0 && index <= size;
    }

    // 检查index索引位置是否可以存在元素
    private void checkElementIndex(int index) {
        if (!isElementIndex(index)) {
            throw new IndexOutOfBoundsException("Index: " + index + ", Size: " + size);
        }
    }

    // 检查index索引位置是否可以添加元素
    private void checkPositionIndex(int index) {
        if (!isPositionIndex(index)) {
            throw new IndexOutOfBoundsException("Index: " + index + ", Size: " + size);
        }
    }

    // 把数组大小扩容或者缩容为newCap
    private void resize(int newCap) {
        E[] temp = (E[]) new Object[newCap];
        // copy数据
        System.arraycopy(data, 0, temp, 0, size);
        data = temp;
    }

    /* toString方法 */
    public String toString() {
        StringBuilder builder = new StringBuilder();
        for(int i = 0;i < size;i++) {
            builder.append(data[i] + " ");
        }
        return builder.toString();
    }

}
```

---

测试Main类

```java
public class Main {
    public static void main(String[] args) {
        MyArrayList<Integer> list = new MyArrayList<Integer>(100);
        list.add(0, 1);
        list.add(1, 2);
        list.add(2, 3);
        System.out.println(list.get(0));
        System.out.println(list.get(1));
        System.out.println(list.get(2));
        System.out.println(list);
    }
}

```
