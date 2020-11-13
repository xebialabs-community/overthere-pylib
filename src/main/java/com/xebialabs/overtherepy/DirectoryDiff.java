/**
 * Copyright 2020 XEBIALABS
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
package com.xebialabs.overtherepy;

import static com.google.common.base.Preconditions.checkArgument;
import static com.google.common.collect.Lists.newArrayList;
import static com.google.common.collect.Maps.newHashMap;
import static com.google.common.collect.Sets.newHashSet;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.Set;

import com.google.common.base.Function;
import com.google.common.base.Predicate;
import com.google.common.collect.Collections2;
import com.google.common.collect.Lists;
import com.google.common.collect.Sets;
import com.google.common.hash.HashCode;
import com.google.common.hash.HashFunction;
import com.google.common.hash.Hashing;
import com.google.common.io.ByteSource;
import com.google.common.io.Files;
import com.xebialabs.overthere.OverthereFile;

/**
 * Compares 2 directories and determines which files were added, removed or changed.
 */
public class DirectoryDiff {

    private final OverthereFile leftSide;
    private final OverthereFile rightSide;
    private final HashFunction hashFunction = Hashing.goodFastHash(32);

    /**
     * Constructor
     *
     * @param leftSide
     *            directory to compare
     * @param rightSide
     *            directory to compare
     */
    public DirectoryDiff(final OverthereFile leftSide, final OverthereFile rightSide) {
        checkArgument(leftSide.isDirectory(), "File [%s] must be a directory.", leftSide);
        checkArgument(rightSide.isDirectory(), "File [%s] must be a directory.", rightSide);
        this.leftSide = leftSide;
        this.rightSide = rightSide;
    }

    /**
     * Calculate the differences between the two directories that this class was constructed with.
     *
     * @return differences
     * @throws IOException
     */
    public DirectoryChangeSet diff() throws IOException {
        DirectoryChangeSet changeSet = new DirectoryChangeSet();
        compareDirectoryRecursive(leftSide, rightSide, changeSet);
        return changeSet;
    }

    /**
     * Calculate an MD5 hash for the given file.
     *
     * @param file
     *            for which MD5 should be calculated.
     * @return MD5 hash
     * @throws IOException
     */
    public static String md5(final OverthereFile file) throws IOException {
        File sourceFile = new File(file.getPath());
        ByteSource source = Files.asByteSource(sourceFile);
        return source.hash(Hashing.md5()).toString();
    }

    /*
     * Intermediate method for recursion, so that objects created in the compareDirectory method can be garbage collected.
     */
    private void compareDirectoryRecursive(final OverthereFile left, final OverthereFile right, final DirectoryChangeSet changeSet)
            throws IOException {
        List<OverthereFile[]> dirsToRecurse = compareDirectory(left, right, changeSet);
        for (OverthereFile[] leftAndRightDir : dirsToRecurse) {
            compareDirectoryRecursive(leftAndRightDir[0], leftAndRightDir[1], changeSet);
        }
    }

    private List<OverthereFile[]> compareDirectory(final OverthereFile left, final OverthereFile right, final DirectoryChangeSet changeSet)
            throws IOException {
        Set<FileWrapper> leftFiles = listFiles(left);
        Set<FileWrapper> rightFiles = listFiles(right);

        // find new files
        Set<FileWrapper> filesAdded = Sets.difference(rightFiles, leftFiles);
        // find removed files
        Set<FileWrapper> filesRemoved = Sets.difference(leftFiles, rightFiles);

        // find changed files
        Set<FileWrapper> potentialChangedFiles = newHashSet(leftFiles);
        potentialChangedFiles.removeAll(filesRemoved);

        // filter out directories
        Map<FileWrapper, FileWrapper> rightFilesIndex = newHashMap();
        for (FileWrapper file : rightFiles) {
            rightFilesIndex.put(file, file);
        }

        Set<FileWrapper> filesChanged = newHashSet();
        for (FileWrapper potentialChangedFile : Sets.filter(potentialChangedFiles, FileWrapperPredicates.FILE)) {
            HashCode leftHash = hash(potentialChangedFile.getFile(), hashFunction);
            FileWrapper rightFile = rightFilesIndex.get(potentialChangedFile);
            HashCode rightHash = hash(rightFile.getFile(), hashFunction);
            if (!leftHash.equals(rightHash)) {
                filesChanged.add(rightFile);
            }
        }

        Function<FileWrapper, OverthereFile> unwrapFunction = new Function<FileWrapper, OverthereFile>() {
            @Override
            public OverthereFile apply(final FileWrapper input) {
                return input.getFile();
            }
        };

        changeSet.getRemoved().addAll(Collections2.transform(filesRemoved, unwrapFunction));
        changeSet.getAdded().addAll(Collections2.transform(filesAdded, unwrapFunction));
        changeSet.getChanged().addAll(Collections2.transform(filesChanged, unwrapFunction));

        Set<FileWrapper> potentialChangedDirectories = Sets.filter(potentialChangedFiles, FileWrapperPredicates.DIRECTORY);
        List<OverthereFile[]> directoriesStillToCheck = newArrayList();
        for (FileWrapper potentialChangedDirectory : potentialChangedDirectories) {
            directoriesStillToCheck.add(
                    new OverthereFile[] { potentialChangedDirectory.getFile(), rightFilesIndex.get(potentialChangedDirectory).getFile() });
        }
        return directoriesStillToCheck;
    }

    private Set<FileWrapper> listFiles(final OverthereFile dir) {
        return newHashSet(Lists.transform(newArrayList(dir.listFiles()), new WrapFile()));
    }

    private HashCode hash(final OverthereFile file, final HashFunction hashFunction) throws IOException {
        File sourceFile = new File(file.getPath());
        ByteSource source = Files.asByteSource(sourceFile);
        return source.hash(hashFunction);
    }

    public static class DirectoryChangeSet {
        private final List<OverthereFile> removed = newArrayList();
        private final List<OverthereFile> added = newArrayList();
        private final List<OverthereFile> changed = newArrayList();

        public List<OverthereFile> getAdded() {
            return added;
        }

        public List<OverthereFile> getChanged() {
            return changed;
        }

        public List<OverthereFile> getRemoved() {
            return removed;
        }

    }

    static class WrapFile implements Function<OverthereFile, FileWrapper> {

        @Override
        public FileWrapper apply(final OverthereFile input) {
            return new FileWrapper(input);
        }
    }

    static class FileWrapper {
        private final OverthereFile file;

        FileWrapper(final OverthereFile file) {
            this.file = file;
        }

        public OverthereFile getFile() {
            return file;
        }

        @Override
        public int hashCode() {
            return file.getName().hashCode();
        }

        @Override
        public boolean equals(final Object obj) {
            if (obj instanceof FileWrapper) {
                return file.getName().equals(((FileWrapper) obj).file.getName());
            }
            return false;
        }

        @Override
        public String toString() {
            return file.toString();
        }
    }

    enum FileWrapperPredicates implements Predicate<FileWrapper> {
        FILE {

            @Override
            public boolean apply(final FileWrapper input) {
                return input.getFile().isFile();
            }
        },
        DIRECTORY {

            @Override
            public boolean apply(final FileWrapper input) {
                return input.getFile().isDirectory();
            }
        }
    }

}
