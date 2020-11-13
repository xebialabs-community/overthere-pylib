/**
 * Copyright 2020 XEBIALABS
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
package com.xebialabs.overtherepy.jython;

import java.io.File;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Enumeration;
import java.util.Vector;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;
import org.python.core.*;

/**
 * The default Jython SyspathJavaLoader does not have the ability to load resources from the classpath.
 * This class adds that ability.
 */
public class PatchedSyspathJavaLoader extends ClassLoader {

    private static final char SLASH_CHAR = '/';

    public PatchedSyspathJavaLoader(final ClassLoader parent) {
        super(parent);
    }

    @Override
    protected Enumeration<URL> findResources(String res) throws IOException {
        Vector<URL> resources = new Vector<URL>();

        PySystemState sys = Py.getSystemState();
        if (res.charAt(0) == SLASH_CHAR) {
            res = res.substring(1);
        }
        String entryRes = res;
        if (File.separatorChar != SLASH_CHAR) {
            res = res.replace(SLASH_CHAR, File.separatorChar);
            entryRes = entryRes.replace(File.separatorChar, SLASH_CHAR);
        }

        PyList path = sys.path;
        for (int i = 0; i < path.__len__(); i++) {
            PyObject entry = replacePathItem(sys, i, path);
            if (entry instanceof SyspathArchive) {
                SyspathArchive archive = (SyspathArchive) entry;

                ZipEntry ze = new ZipFile(new File(archive.asString())).getEntry(entryRes);
                if (ze != null) {
                    try {
                        resources.add(new URL("jar:file:" + entry.__str__().toString() + "!/" + entryRes));
                    } catch (MalformedURLException e) {
                        throw new RuntimeException(e);
                    }
                }
                continue;
            }
            if (!(entry instanceof PyUnicode)) {
                entry = entry.__str__();
            }
            String dir = sys.getPath(entry.toString());
            try {
                File resource = new File(dir, res);
                if (!resource.exists()) {
                    continue;
                }
                resources.add(resource.toURI().toURL());
            } catch (MalformedURLException e) {
                throw new RuntimeException(e);
            }
        }
        return resources.elements();
    }

    PyObject replacePathItem(PySystemState sys, int idx, PyList paths) {
        PyObject path = paths.__getitem__(idx);
        if (path instanceof SyspathArchive) {
            // already an archive
            return path;
        }

        try {
            // this has the side affect of adding the jar to the PackageManager during the
            // initialization of the SyspathArchive
            path = new SyspathArchive(sys.getPath(path.toString()));
        } catch (Exception e) {
            return path;
        }
        paths.__setitem__(idx, path);
        return path;
    }


}
