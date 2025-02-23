import { Button } from "@/components/ui/button";
import {
    RiFacebookFill,
    RiGithubFill,
    RiGoogleFill,
    RiTwitterXFill,
} from "@remixicon/react";

export default function SocialAuthentication() {
    return (
        <div className="flex flex-wrap gap-2 w-full justify-around px-6 md:px-12">
            <Button
                variant="outline"
                aria-label="Login with Google"
                size="icon"
                disabled>
                <RiGoogleFill
                    className="dark:text-primary text-[#DB4437]"
                    size={16}
                    aria-hidden="true"
                />
            </Button>
            <Button
                variant="outline"
                aria-label="Login with Facebook"
                size="icon"
                disabled>
                <RiFacebookFill
                    className="dark:text-primary text-[#1877f2]"
                    size={16}
                    aria-hidden="true"
                />
            </Button>
            <Button
                variant="outline"
                aria-label="Login with X"
                size="icon"
                disabled>
                <RiTwitterXFill
                    className="dark:text-primary text-[#14171a]"
                    size={16}
                    aria-hidden="true"
                />
            </Button>
            <Button
                variant="outline"
                aria-label="Login with GitHub"
                size="icon"
                disabled>
                <RiGithubFill
                    className="dark:text-primary text-black"
                    size={16}
                    aria-hidden="true"
                />
            </Button>
        </div>
    );
}
