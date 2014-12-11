/**
 * Copyright (c) 2008-2014, XebiaLabs B.V., All rights reserved.
 *
 *
 * Overtherepy is licensed under the terms of the GPLv2
 * <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>, like most XebiaLabs Libraries.
 * There are special exceptions to the terms and conditions of the GPLv2 as it is applied to
 * this software, see the FLOSS License Exception
 * <http://github.com/xebialabs/overthere/blob/master/LICENSE>.
 *
 * This program is free software; you can redistribute it and/or modify it under the terms
 * of the GNU General Public License as published by the Free Software Foundation; version 2
 * of the License.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
 * without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with this
 * program; if not, write to the Free Software Foundation, Inc., 51 Franklin St, Fifth
 * Floor, Boston, MA 02110-1301  USA
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
