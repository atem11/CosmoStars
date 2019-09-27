package tools.grabber;


import java.io.File;
import java.nio.file.Path;

public interface Grubber {

    public void grub(Path output, File list);
}
